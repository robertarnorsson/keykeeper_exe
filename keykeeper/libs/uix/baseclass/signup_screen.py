from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield.textfield import MDTextField
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.properties import StringProperty

import re
import os
from concurrent.futures import ThreadPoolExecutor

from hash import hash_password, generate_salt, generate_pepper
from encryption import Security
from get_sys import getSystemInfo
from utils import make_uuid, replace_settings
from database import make_users_table, create_iuser_database, save_user, retrieve_users
from constants import PROJECT_DIR, BASE_SETTINGS, BASE_FILTERS
        
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
    
class PasswordTextField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class SignupScreen(Screen):

    def __init__(self):
        super().__init__()

        Window.bind(on_keyboard=self._handle_keyboard)

        self.app = MDApp.get_running_app()

        self.is_making = False
    
    def _handle_keyboard(self, instance, key, *args):
        if self.manager.current == 'signup':
            if key == 13:
                self.start_make_user()
    
    def on_enter(self, *args):
        self.app.theme_cls.theme_style = "Dark"
        self.app.theme_cls.primary_palette = "Red"
        self.app.theme_cls.primary_hue = "500"
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        self.ids['name'].text = ""
        self.ids['password'].ids['text_field'].text = ""
        return super().on_pre_leave(*args)

    def start_make_user(self):
        if not self.is_making:
            self.is_making = True
            self.ids['signupbtn'].text = "Saving user..."
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.future = self.executor.submit(self.make_user)
            self.future.add_done_callback(self.handle_result)

    def handle_result(self, future):
        valid = future.result()
        Clock.schedule_once(lambda dt: self.cleanup(valid), 0)
    
    def cleanup(self, valid):
        self.ids['signupbtn'].text = "Sign Up"
        self.is_making = False
        print(valid)
        if valid:
            self.goto_screen('login', 'right')
        else:
            print("No input given.")

    def make_user(self):
        name = self.ids['name'].text
        password = self.ids['password'].ids['text_field'].text

        users = retrieve_users()
        users_name = []
        for user in users:
            users_name.append(user[1])

        if name in users_name:
            print("Name already taken!")
            return False

        if password == "":
            print("Some input is empty")
            return False

        user_uuid = str(make_uuid())

        os.mkdir(f'{PROJECT_DIR}\\database\\{user_uuid}')
        os.mkdir(f'{PROJECT_DIR}\\database\\{user_uuid}\\data')

        replace_settings(user_uuid, BASE_SETTINGS)

        SYS = getSystemInfo()

        ENC = Security(5)

        sys_pw = str(password+SYS["hostname"]+SYS["processor"]).replace(" ", "")

        sltp = generate_salt(32)
        pepp = generate_pepper(32)

        hsh_pw = hash_password(sys_pw, sltp, pepp)
        
        enc_hsh_pw = ENC.encrypt(hsh_pw, str(password[:int(len(password)/1.32)]+((SYS['hostname']).lower())[int(len(SYS['hostname'])/2.63):]+(password[:int(len(password)/2.75)]).title()+str(((password[int(len(password)/1.55):]).upper()).title())+password[:int(len(password)/3.97)]+(SYS['hostname'])[:int(len(SYS['hostname'])/2.86)]))
        enc_sltp = ENC.encrypt(sltp, str(password[int(len(password)/2.54):] + password[int(len(password)/2.73):] + (SYS['hostname'])[:int(len(SYS['hostname'])/1.65)] + password[:int(len(password)/3.74)] + (SYS['hostname']).lower()[int(len(SYS['hostname'])/2.13):int(len(SYS['hostname'])/1.5)] + password[:int(len(password)/4.24)]))
        enc_pepp = ENC.encrypt(pepp, str((SYS['hostname'])[:int(len(SYS['hostname'])/2.14)] + password[int(len(password)/3.14):] + password[int(len(password)/2.25):] + password[int(len(password)/2.18):] + (SYS['hostname']).lower()[int(len(SYS['hostname'])/3.33):] + password[:int(len(password)/4.63)]))

        make_users_table()

        for bfilter in BASE_FILTERS:
            if bfilter == "":
                continue
            create_iuser_database(user_uuid, bfilter)

        save_user('users', user_uuid, name, enc_hsh_pw, enc_sltp, enc_pepp)

        return True
    
    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
