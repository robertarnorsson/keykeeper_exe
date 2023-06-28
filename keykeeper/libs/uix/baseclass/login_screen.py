from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty

import re
from concurrent.futures import ThreadPoolExecutor

from hash import verify_password
from encryption import Security
from utils import set_keyring, encode_b64
from database import retrieve_user_by_name, make_users_table
from constants import SYS
from session import Session
        
class CredInputPL(MDTextField):
    def insert_text(self, substring, from_undo=False):
        password_valid = r'^[A-Za-z\d@$!%*#?&]$'
        s = substring
        if substring == '\n':
            s = ""
        if len(self.text) > 64:
            s = ""
        if not re.match(password_valid, substring):
            s = ""
        return super().insert_text(s, from_undo=from_undo)
    
class PasswordTextFieldL(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class LoginScreen(Screen):
    def __init__(self):
        super().__init__()

        Window.bind(on_keyboard=self._handle_keyboard)

        self.is_loggin_in = False

        self.app = MDApp.get_running_app()
    
    def _handle_keyboard(self, instance, key, *args):
        if self.manager.current == 'login':
            if key == 13:
                self.start_check_login()

    def on_enter(self, *args):
        self.app.theme_cls.theme_style = 'Dark'
        self.app.theme_cls.primary_palette = 'Red'
        self.app.theme_cls.primary_hue = '500'
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        self.ids['name'].text = ""
        self.ids['password'].ids['text_field'].text = ""
        return super().on_pre_leave(*args)

    def start_check_login(self):
        if self.is_loggin_in:
            return
        
        if self.ids['password'].ids['text_field'].text == "":
            return
        
        self.is_loggin_in = True
        self.ids['loginbtn'].text = "Validating..."
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = self.executor.submit(self.check_login)
        self.future.add_done_callback(self.handle_result)

    def handle_result(self, future):
        valid_login = future.result()
        Clock.schedule_once(lambda dt: self.cleanup(valid_login), 0)

    def cleanup(self, valid):
        self.ids['loginbtn'].text = "Login"
        self.is_loggin_in = False
        if valid:
            self.goto_screen('main', 'up')
        else:
            print("Wrong password")

    def check_login(self):
        name = self.ids['name'].text
        password = self.ids['password'].ids['text_field'].text

        user = retrieve_user_by_name(name)

        if len(user) == 0:
            print("A user with that name does not exist")
            return False

        ENC = Security(5)

        user_uuid = user[0]
        user_name = user[1]
        user_password = user[2]
        user_sltup = user[3]
        user_pepup = user[4]

        sys_pw = str(password+SYS['hostname']+SYS['processor']).replace(" ", "")

        try:
            dec_hsh_pw = ENC.decrypt(user_password, str(password[:int(len(password)/1.32)]+((SYS['hostname']).lower())[int(len(SYS['hostname'])/2.63):]+(password[:int(len(password)/2.75)]).title()+str(((password[int(len(password)/1.55):]).upper()).title())+password[:int(len(password)/3.97)]+(SYS['hostname'])[:int(len(SYS['hostname'])/2.86)]))
            dec_sltp = ENC.decrypt(user_sltup, str(password[int(len(password)/2.54):] + password[int(len(password)/2.73):] + (SYS['hostname'])[:int(len(SYS['hostname'])/1.65)] + password[:int(len(password)/3.74)] + (SYS['hostname']).lower()[int(len(SYS['hostname'])/2.13):int(len(SYS['hostname'])/1.5)] + password[:int(len(password)/4.24)]))
            dec_pepp = ENC.decrypt(user_pepup, str((SYS['hostname'])[:int(len(SYS['hostname'])/2.14)] + password[int(len(password)/3.14):] + password[int(len(password)/2.25):] + password[int(len(password)/2.18):] + (SYS['hostname']).lower()[int(len(SYS['hostname'])/3.33):] + password[:int(len(password)/4.63)]))

            pw_ver = verify_password(dec_hsh_pw, sys_pw, dec_sltp, dec_pepp)
            if pw_ver:
                print("ACCESS GRANTED")
                Session.USER_UUID = user_uuid
                Session.NAME = user_name
                save_pw = encode_b64(password, 'ascii')
                set_keyring(f'KeyKeeper - {user_uuid}', user_uuid, save_pw)
                return True
            else:
                return False
        except:
            print("Something does not add up!")
        return False
        
    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
