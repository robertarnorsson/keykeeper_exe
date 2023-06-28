from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty

import os
import re

from session import Session
from database import create_iuser_database
from constants import USERS_PATH

class FilterButton(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()

class FilterTextField(MDTextField):
    def insert_text(self, substring, from_undo=False):
        name_valid = r'^[a-zA-Z0-9]+$'
        s = substring
        if substring == '\n':
            s = ""
        if len(self.text) >= 12:
            s = ""
        if not re.match(name_valid, substring):
            s = ""
        return super().insert_text(s, from_undo=from_undo)

class NewFilterScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        Window.bind(on_keyboard=self._handle_keyboard)

        self.pw_icon = "key-variant"
        self.icon_disabled = False
        self.icon_disabled_icon = 'cancel'
        self.icon_disabled_icon_icon = ''

        self.icon_list = [
            'key-variant',
            'home',
            'briefcase',
            'school'
        ]

        self.filter_list = os.listdir(f'{USERS_PATH}\\{Session.USER_UUID}\\data')

        self.menu_items_filter = [
            {   
                "viewclass": "OneLineListItem",
                "text": (i.split(".")[0]).capitalize(),
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
        if self.manager.current == 'newfilter':
            if key == 275 or key == 273:
                self.cycle_icon('left')
            if key == 276 or key == 274:
                self.cycle_icon('right')
    
    def on_pre_leave(self, *args):
        self.ids['filter_text'].text = ""
        return super().on_pre_leave(*args)

    def update_filter_menu(self):
        self.filter_list = os.listdir(f'{USERS_PATH}\\{Session.USER_UUID}\\data')

        self.menu_items_filter = [
            {
                "viewclass": "OneLineListItem",
                "text": (i.split(".")[0]).capitalize(),
                "icon": "git",
                "on_release": lambda x=i: self.menu_filter_callback(x),
            } for i in self.filter_list
        ]

        self.menu_filter.items = self.menu_items_filter

        Session.FILTER = (self.filter_list[0].split(".")[0]).capitalize()

        self.ids['filter_container'].ids['filter_button'].text = (Session.FILTER.split(".")[0]).capitalize()

    def menu_filter_callback(self, text_item):
        self.menu_filter.dismiss()
        print(text_item)
        self.ids['filter_container'].ids['filter_button'].text = (text_item.split(".")[0]).capitalize()
        Session.FILTER = (text_item.split(".")[0]).lower()
        
    """def cycle_icon(self, dir):
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
            self.icon_disabled = True"""

    def save_new_filter(self):
        filter_name = self.ids['filter_text'].text
        #icon = self.pw_icon if not self.icon_disabled else ''

        self.filter_list = os.listdir(f'{USERS_PATH}\\{Session.USER_UUID}\\data')
        filter_list = []

        for _filter in self.filter_list:
            filter_list.append((_filter.split(".")[0]).lower())

        filter_name_l = filter_name.lower()
        filter_name_l = filter_name_l.replace("'", "")
        filter_name_l = filter_name_l.replace('"', "")

        if filter_name_l == "":
            print("Some inputs are empty!")
            return

        if filter_name_l in filter_list:
            print(f'Filter name "{filter_name_l}" is already taken! Please choose a different name.')
            self.ids['filter_text'].text = ""
            return
        
        create_iuser_database(Session.USER_UUID, filter_name_l)
        self.update_filter_menu()

        self.ids['filter_text'].text = ""
    
    def remove_filter(self):
        self.filter_list_len = len(os.listdir(f'{USERS_PATH}\\{Session.USER_UUID}\\data'))
        
        if self.filter_list_len > 1:
            os.remove(f'{USERS_PATH}\\{Session.USER_UUID}\\data\\{Session.FILTER}.db')
            self.update_filter_menu()
        else:
            print("One filter is required")
            return

    def on_pre_enter(self, *args):
        self.ids['filter_container'].ids['filter_button'].text = Session.FILTER.capitalize()
        return super().on_pre_enter(*args)

    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
    pass
