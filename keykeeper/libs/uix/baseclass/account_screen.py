from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

import shutil

from utils import logout
from session import Session
from constants import USERS_PATH
from database import delete_user_by_uuid

class AccountScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def show_dialog(self, title, text, buttons, dismiss_button):
        all_buttons = []
        if dismiss_button:
            dismiss_btn = MDFlatButton(text="Close", on_release=self.close_dialog)
            all_buttons.append(dismiss_btn)
        for button in buttons:
            new_button = MDFlatButton(text=button[0], on_release=button[1])
            all_buttons.append(new_button)
        self.dialog = MDDialog(title=title, text=text, size_hint=(0.7, None), size_hint_max_x=550, height=150, buttons=all_buttons)
        self.dialog.open()
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
    
    def start_delete_account(self):
        self.show_dialog("Are you sure?", "Are you sure you want to delete your account?\nThis action will remove every password that has been saved and totally remove the account.", [["Cancel", self.close_dialog], ["Delete", self.delete_account]], False)
    
    def delete_account(self, *args):
        print("Delete account")
        self.close_dialog()
        print(f'{USERS_PATH}\\{Session.USER_UUID}\\')
        shutil.rmtree(f'{USERS_PATH}\\{Session.USER_UUID}\\')
        delete_user_by_uuid(Session.USER_UUID)
        self.log_out()
    
    def log_out(self, *args):
        logout()
        self.goto_screen('login', 'down')
    
    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
    
    pass
