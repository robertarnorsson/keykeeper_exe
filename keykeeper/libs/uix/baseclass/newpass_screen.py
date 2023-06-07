from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty

import os
import re
from concurrent.futures import ThreadPoolExecutor

from session import Session
from database import save_password, retrieve_password_by_title
from constants import PROJECT_DIR
from encryption import Security
from utils import get_settings, get_keyring, decode_b64

class FilterButton(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()

class CredInputP(MDTextField):
    def insert_text(self, substring, from_undo=False):
        password_valid = r"^[A-Za-z\d@$!%*#?&]$"
        s = substring
        if substring == '\n':
            s = ""
        if len(self.text) > 64:
            s = ""
        if not re.match(password_valid, substring):
            s = ""
        return super().insert_text(s, from_undo=from_undo)
    
class PasswordTextFieldNP(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class Item(OneLineIconListItem):
    left_icon = StringProperty()

class NewPassScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        Window.bind(on_keyboard=self._handle_keyboard)

        self.is_making = False

        self.pw_icon = "key-variant"
        self.icon_disabled = False
        self.icon_disabled_icon = 'cancel'
        self.icon_disabled_icon_icon = ''

        self.icon_list = [
            'key-variant',
            'home',
            'briefcase',
            'school',
            'wifi'
        ]

        self.filter_list = os.listdir(f'{PROJECT_DIR}\\database\\{Session.USER_UUID}\\data')

        self.menu_items_filter = [
            {
                "text": (i.split(".")[0]).capitalize(),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_filter_callback(x),
            } for i in self.filter_list
        ]

        self.menu_filter = MDDropdownMenu(
            caller=self.ids['filter_container'].ids['filter_button'],
            items=self.menu_items_filter,
            max_height=dp(150),
            position="bottom",
            width_mult=4,
        )
    
    def _handle_keyboard(self, instance, key, *args):
        if self.manager.current == 'newpassword':
            if key == 275 or key == 273:
                self.cycle_icon('left')
            if key == 276 or key == 274:
                self.cycle_icon('right')
    
    def on_pre_enter(self, *args):
        self.ids['filter_container'].ids['filter_button'].text = Session.FILTER.capitalize()
        return super().on_pre_enter(*args)
    
    def on_pre_leave(self, *args):
        self.ids['title_text'].text = ""
        self.ids['username_text'].text = ""
        self.ids['password_text'].ids['text_field'].text = ""
        return super().on_pre_leave(*args)

    def menu_filter_callback(self, text_item):
        self.menu_filter.dismiss()
        print(text_item)
        self.ids['filter_container'].ids['filter_button'].text = (text_item.split(".")[0]).capitalize()
        Session.FILTER = (text_item.split(".")[0]).lower()
        
    def cycle_icon(self, dir):
        if self.icon_disabled:
            return
        button = self.ids['icon_select']
        total_len = len(self.icon_list)-1
        index = self.icon_list.index(self.pw_icon)
        print(total_len, index)
        if dir == 'right':
            if index < 0:
                index = total_len+1
            self.pw_icon = self.icon_list[index-1]
            button.icon = self.pw_icon
            return

        if dir == 'left':
            if index == total_len:
                index = -1
            self.pw_icon = self.icon_list[index+1]
            button.icon = self.pw_icon
            return

    def disable_icon(self):
        button = self.ids['icon_select']
        if self.icon_disabled:
            button.icon = self.icon_list[self.icon_list.index(self.pw_icon)]
            self.icon_disabled = False
        else:
            button.icon = self.icon_disabled_icon
            self.icon_disabled = True
        
    def start_save_newpass(self):
        if not self.is_making:
            self.is_making = True
            self.ids['save_button'].text = 'Saving password...'
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.future = self.executor.submit(self.save_new_password)
            self.future.add_done_callback(self.handle_result)
    
    def handle_result(self, future):
        valid = future.result()
        Clock.schedule_once(lambda dt: self.cleanup(valid), 0)
    
    def cleanup(self, valid):
        self.ids['save_button'].text = "Save Password"
        self.is_making = False
        if valid:
            self.goto_screen('main', 'left')
            self.ids['title_text'].text = ""
            self.ids['username_text'].text = ""
            self.ids['password_text'].ids['text_field'].text = ""
        else:
            self.ids['title_text'].text = ""

    def save_new_password(self):
        title = self.ids['title_text'].text
        username = self.ids['username_text'].text
        password = self.ids['password_text'].ids['text_field'].text
        icon = self.pw_icon if not self.icon_disabled else ''
        if title == "" or username == "" or password == "":
            print("Some inputs are empty!")
            return False
        
        if_exists_password = retrieve_password_by_title(Session.FILTER, Session.USER_UUID, title)

        if if_exists_password != None:
            print("That name is already taken! Please choose a different name.")
            return False
        
        b64password = get_keyring(f'KeyKeeper - {Session.USER_UUID}', Session.USER_UUID)
        decode_pw = decode_b64(b64password, 'ascii')

        lvl = get_settings('encryption', 'level')
        
        ENC = Security(lvl)
        
        enc_un = ENC.encrypt(username, decode_pw)
        enc_pw = ENC.encrypt(password, decode_pw)
        
        save_password(Session.FILTER, Session.USER_UUID, title, enc_un, enc_pw, icon, lvl)

        return True

    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
    pass
