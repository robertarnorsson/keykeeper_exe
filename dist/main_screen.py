from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.effects.fadingedge.fadingedge import FadingEdgeEffect
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty

import os
from concurrent.futures import ThreadPoolExecutor

from session import Session
from constants import PROJECT_DIR
from database import retrieve_passwords, retrieve_password_by_title, update_password_by_title, delete_password_by_title, retrieve_lvl_by_title
from utils import logout, get_keyring, decode_b64, get_settings
from encryption import Security

class FadeScrollView(FadingEdgeEffect, ScrollView):
    pass

class PasswordButton(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()
    height_p = NumericProperty(60)

class FilterButton(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()

class PasswordTextFieldM(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class MainScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.title = ""

        self.is_decrypting = False
        self.is_changing = False

        filter_list = os.listdir(f'{PROJECT_DIR}\\database\\{Session.USER_UUID}\\data')

        self.menu_items_filter = [
            {
                "text": (i.split(".")[0]).capitalize(),
                "viewclass": "OneLineListItem",
                "height": dp(55),
                "on_release": lambda x=i: self.menu_filter_callback(x),
            } for i in filter_list
        ]

        self.menu_filter = MDDropdownMenu(
            caller=self.ids['filter_container'].ids['filter_button'],
            items=self.menu_items_filter,
            position="bottom",
            width_mult=4,
        )
    
    def update_filter_menu(self):
        self.filter_list = os.listdir(f'{PROJECT_DIR}\\database\\{Session.USER_UUID}\\data')

        self.menu_items_filter = [
            {
                "text": (i.split(".")[0]).capitalize(),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_filter_callback(x),
            } for i in self.filter_list
        ]

        self.menu_filter.items = self.menu_items_filter
    
    def menu_filter_callback(self, text_item):
        self.menu_filter.dismiss()
        self.ids['filter_container'].ids['filter_button'].text = (text_item.split(".")[0]).capitalize()
        Session.FILTER = (text_item.split(".")[0]).lower()
        self.load_passwords()
    
    def check_empty_pass(self):
        self.container = self.ids['scroll_container']
        children = self.container.children

        if children != []:
            return
        
        top_padding = MDBoxLayout(
            size_hint=(1, 0.381967)
        )
        
        text = MDLabel(
            size_hint=(1, 1),
            text="You have not saved any passwords yet!",
            font_style='Body1',
            halign='center',
            valign='center',
            theme_text_color='Hint'
        )

        self.container.add_widget(top_padding)
        self.container.add_widget(text)
    
    def on_pre_enter(self, *args):
        self.load_data()
        self.update_filter_menu()
        if Session.FILTER == "":
            self.ids['filter_container'].ids['filter_button'].text = (os.listdir(f'{PROJECT_DIR}\\database\\{Session.USER_UUID}\\data')[0].split(".")[0]).capitalize()
            Session.FILTER = (os.listdir(f'{PROJECT_DIR}\\database\\{Session.USER_UUID}\\data')[0].split(".")[0]).capitalize()
        else:
            self.ids['filter_container'].ids['filter_button'].text = Session.FILTER.capitalize()   
        self.load_passwords()
        self.ids['account_button_long'].text = Session.NAME
        self.check_empty_pass()
        self.update_slider_text(1)
        self.parent.app.theme_cls.theme_style = get_settings('color', 'theme')
        self.parent.app.theme_cls.primary_palette = get_settings('color', 'primary')
        return super().on_pre_enter(*args)
    
    def on_leave(self, *args):
        self.ids['dail'].close_stack()
        self.clear_password()
        return super().on_leave(*args)

    def update_slider_text(self, value):
        value = int(value)
        if value <= 3:
            self.ids['slider_text'].text = f'Level: {value} (Bad)'
        elif value <= 7:
            self.ids['slider_text'].text = f'Level: {value} (Good)'
        else:
            self.ids['slider_text'].text = f'Level: {value} (Super)'

    def clear_password(self, *largs):
        self.title = ""
        self.ids['title_text'].text = ""
        self.ids['username_text'].text = ""
        self.ids['password_text'].ids['text_field'].text = ""

    def load_passwords(self):
        self.clear_password()
        passwords = retrieve_passwords((Session.FILTER).lower(), Session.USER_UUID)
        self.container = self.ids['scroll_container']
        self.container.clear_widgets()
        if passwords == []:
            self.check_empty_pass()
        for pw in passwords:
            button = PasswordButton(
                text=pw[0],
                icon=pw[3]
            )
            self.container.add_widget(button)

    def load_data(self):
        self.data = {
            'New Password': [
                'key-plus',
                'on_release', self.new_password
            ],
            'New Filter': [
                'filter-plus',
                'on_release', self.new_filter
            ],
            'Settings': [
                'cog',
                'on_release', self.settings
            ],
            'Sign Out': [
                'logout',
                'on_release', self.log_out
            ]
        }
        self.ids['dail'].data = self.data
    
    def show_password(self, title):
        info = retrieve_password_by_title(Session.FILTER, Session.USER_UUID, title)[0]

        title = info[0]
        enc_un = info[1]
        enc_pw = info[2]
        lvl = info[4]

        self.start_decrypt(title, enc_un, enc_pw, lvl)
        self.title = title
        
    def start_decrypt(self, ti, un, pw, lvl):
        if not self.is_decrypting:
            self.is_decrypting = True
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.future = self.executor.submit(lambda: self.do_decrypter(ti, un, pw, lvl))
            self.future.add_done_callback(self.handle_result)
            self.ids['title_text'].text = "Decrypting..."
            self.ids['username_text'].text = "Please wait..."
            self.ids['password_text'].ids['text_field'].text = "Decrypting..."
            self.ids['enc_lvl_slider'].value = 1
            self.ids['enc_lvl_slider'].disabled = True
    
    def handle_result(self, future):
        dec_cred = future.result()
        Clock.schedule_once(lambda dt: self.cleanup(dec_cred), 0)
    
    def cleanup(self, dec_cred):
        if dec_cred:
            self.ids['title_text'].text = dec_cred[0]
            self.ids['username_text'].text = dec_cred[1]
            self.ids['password_text'].ids['text_field'].text = dec_cred[2]
            self.ids['enc_lvl_slider'].value = dec_cred[3]
            self.update_slider_text(dec_cred[3])
            self.ids['enc_lvl_slider'].disabled = False
            self.is_decrypting = False
        else:
            print("Something went wrong! Most likely decryption of the password.")
            self.clear_password()
            self.is_decrypting = False
    
    def do_decrypter(self, title: str, enc_username: str, enc_password: str, lvl: int):
        b64password = get_keyring(f'KeyKeeper - {Session.USER_UUID}', Session.USER_UUID)
        decode_pw = decode_b64(b64password, 'ascii')

        ENC = Security(lvl)

        try:
            dec_un = ENC.decrypt(enc_username, decode_pw)
            dec_pw = ENC.decrypt(enc_password, decode_pw)
            return [title, dec_un, dec_pw, lvl]
        except:
            return []

    def start_change_password(self, title):
        if not self.is_changing:
            self.is_changing = True
            new_title = self.ids['title_text'].text
            username = self.ids['username_text'].text
            password = self.ids['password_text'].ids['text_field'].text
            self.ids['title_text'].text = "Decrypting..."
            self.ids['username_text'].text = "Please wait..."
            self.ids['password_text'].ids['text_field'].text = "Decrypting..."
            self.ids['enc_lvl_slider'].disabled = True
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.future = self.executor.submit(lambda: self.change_password(new_title, username, password))
            self.future.add_done_callback(self.handle_result_cp)
    
    def handle_result_cp(self, future):
        value = future.result()
        Clock.schedule_once(lambda dt: self.cleanup_cp(value), 0)

    def cleanup_cp(self, value):
        if value:
            print("Saved")
            self.load_passwords()
            self.is_changing = False
            self.ids['enc_lvl_slider'].disabled = False
        else:
            print("Something happend")
            self.load_passwords()
            self.is_changing = False
            self.ids['enc_lvl_slider'].disabled = False

    def change_password(self, new_title, username, password):
        if self.title == "":
            return False
        info = retrieve_password_by_title(Session.FILTER, Session.USER_UUID, self.title)[0]
        icon = info[3]
        lvl = int(info[4])
        if info[0] == new_title and info[1] == username and info[2] == password and info[3] == icon:
            return False

        b64password = get_keyring(f'KeyKeeper - {Session.USER_UUID}', Session.USER_UUID)
        decode_pw = decode_b64(b64password, 'ascii')

        lvl = int(self.ids['enc_lvl_slider'].value)
        
        ENC = Security(lvl)
        
        enc_un = ENC.encrypt(username, decode_pw)
        enc_pw = ENC.encrypt(password, decode_pw)

        update_password_by_title(Session.FILTER, Session.USER_UUID, self.title, new_title, enc_un, enc_pw, icon, lvl)
        self.title = new_title
        return True
    
    def delete_password(self):
        if self.title == "":
            return
        if self.is_decrypting or self.is_changing:
            return
        delete_password_by_title(Session.FILTER, Session.USER_UUID, self.title)
        self.title = ""
        self.ids['title_text'].text = ""
        self.ids['username_text'].text = ""
        self.ids['password_text'].ids['text_field'].text = ""
        self.load_passwords()
        self.check_empty_pass()
        
    def new_password(self, *args):
        self.goto_screen('newpassword', 'right')
    
    def new_filter(self, *args):
        self.goto_screen('newfilter', 'right')
    
    def settings(self, *args):
        self.goto_screen('settings', 'up')

    def log_out(self, *args):
        logout()
        self.goto_screen('login', 'down')

    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
    pass
