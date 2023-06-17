from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.color_definitions import colors
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import StringProperty

from utils import get_settings, update_settings

class FilterButton(MDRelativeLayout):
    text = StringProperty()
    icon = StringProperty()

class SettingsScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.theme = 'Dark'
        self.primary = 'Red'
        self.hue = "500"

        self.need_restart = False

        self.old_theme = self.theme
        self.old_primary = self.primary
        self.old_hue = self.hue

        self.colors = {
            "red": get_color_from_hex(colors['Red'][self.hue]),
            "pink": get_color_from_hex(colors['Pink'][self.hue]),
            "purple": get_color_from_hex(colors['Purple'][self.hue]),
            "blue": get_color_from_hex(colors['Blue'][self.hue]),
            "cyan": get_color_from_hex(colors['Cyan'][self.hue]),
            "teal": get_color_from_hex(colors['Teal'][self.hue]),
            "green": get_color_from_hex(colors['Green'][self.hue]),
            "yellow": get_color_from_hex(colors['Yellow'][self.hue]),
            "orange": get_color_from_hex(colors['Orange'][self.hue]),
        }

        self.menu_items_filter = [
            {
                "text": i.capitalize(),
                "bg_color": get_color_from_hex(colors[i.capitalize()][self.hue]),
                "theme_text_color": 'Custom',
                "viewclass": "OneLineListItem",
                "height": dp(55),
                "on_release": lambda x=i: self.menu_filter_callback(x),
            } for i in self.colors
        ]

        self.menu_filter = MDDropdownMenu(
            caller=self.ids['filter_container'].ids['filter_button'],
            items=self.menu_items_filter,
            position="bottom",
            width_mult=4,
        )
    
    def menu_filter_callback(self, color):
        self.menu_filter.dismiss()
        self.update_colors()
        self.ids['filter_container'].text = color.capitalize()
        self.ids['filter_container'].ids['filter_button'].md_bg_color = self.colors[color]
        self.ids['filter_container'].ids['filter_button'].line_color = self.colors[color]
        self.ids['color_hue_slider'].color = self.colors[color]
        self.ids['color_hue_slider'].thumb_color_active = self.colors[color]
        self.ids['color_hue_slider'].thumb_color_inactive = self.colors[color]
        self.primary = color.capitalize()
        self.need_restart = True

    def show_dialog(self, title, text, buttons):
        all_buttons = []
        dismiss_btn = MDFlatButton(text="Close", on_release=self.close_dialog)
        all_buttons.append(dismiss_btn)
        for button in buttons:
            new_button = MDFlatButton(text=button[0], on_release=button[1])
            all_buttons.append(new_button)
        self.dialog = MDDialog(title=title, text=text, size_hint=(0.7, None), size_hint_max_x=550, height=150, buttons=all_buttons)
        self.dialog.open()
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
    
    def update_colors(self):
        self.colors = {
            "red": get_color_from_hex(colors['Red'][self.hue]),
            "pink": get_color_from_hex(colors['Pink'][self.hue]),
            "purple": get_color_from_hex(colors['Purple'][self.hue]),
            "blue": get_color_from_hex(colors['Blue'][self.hue]),
            "cyan": get_color_from_hex(colors['Cyan'][self.hue]),
            "teal": get_color_from_hex(colors['Teal'][self.hue]),
            "green": get_color_from_hex(colors['Green'][self.hue]),
            "yellow": get_color_from_hex(colors['Yellow'][self.hue]),
            "orange": get_color_from_hex(colors['Orange'][self.hue]),
        }
    
    def apply_close(self, *args):
        self.apply_settings()
        self.check_changes()
        self.close_dialog()
    
    def close_application(self, *args):
        update_settings('color', 'theme', self.theme)
        update_settings('color', 'primary', self.primary)
        update_settings('color', 'hue', self.hue)
        MDApp.get_running_app().stop()

    def on_pre_enter(self, *args):
        self.theme = get_settings('color', 'theme')
        self.old_theme = self.theme
        self.ids['theme_switch'].active = True if self.theme == 'Light' else False
        self.ids['theme_switch_text'].text = f'{self.theme} theme'
        self.ids['theme_icon'].icon = "brightness-7" if self.theme == 'Light' else "brightness-2"

        self.primary = get_settings('color', 'primary')
        self.old_primary = self.primary
        self.ids['filter_container'].text = self.primary

        self.hue = get_settings('color', 'hue')
        self.old_hue = self.hue
        self.ids['color_hue_slider'].value = int(self.hue)
        self.ids['slider_text'].text = str(int(self.hue))
        self.update_colors()
        self.ids['filter_container'].ids['filter_button'].md_bg_color = self.colors[self.primary.lower()]
        self.ids['filter_container'].ids['filter_button'].line_color = self.colors[self.primary.lower()]
        return super().on_pre_enter(*args)

    def switch_theme(self, instance, value, revert):
        if revert:
            if self.theme == 'Light':
                self.ids['theme_icon'].icon = "brightness-7"
            else:
                self.ids['theme_icon'].icon = "brightness-2"
        else:
            if value:
                self.theme = 'Light'
                self.ids['theme_icon'].icon = "brightness-7"
            else: 
                self.theme = 'Dark'
                self.ids['theme_icon'].icon = "brightness-2"
            
            self.need_restart = True

        self.ids['theme_switch_text'].text = f'{self.theme} theme'
    
    def update_hue(self, revert, *args):
        slider = self.ids['color_hue_slider']
        slider_text = self.ids['slider_text']

        if revert:
            slider.value = int(self.hue)
        else:
            self.hue = str(int(slider.value))
        
            slider_text.text = str(int(slider.value))
            self.hue = str(int(slider.value))

            self.update_colors()

            self.ids['filter_container'].ids['filter_button'].md_bg_color = self.colors[self.primary.lower()]
            self.ids['filter_container'].ids['filter_button'].line_color = self.colors[self.primary.lower()]

            slider.color = self.colors[self.primary.lower()]
            slider.thumb_color_active = self.colors[self.primary.lower()]
            slider.thumb_color_inactive = self.colors[self.primary.lower()]

            self.need_restart = True
    
    def revert_settings(self, *args):
        self.theme = self.old_theme
        self.primary = self.old_primary
        self.hue = self.old_hue

        self.close_dialog()
        self.goto_screen('main', 'down')
        
    def apply_settings(self):
        if self.need_restart:
            if self.theme == self.old_theme and self.primary == self.old_primary and self.hue == self.old_hue:
                return
            self.show_dialog("Needs Restart", "You have to restart the application\nClicking restart will close the application", [["Restart", self.close_application]])
            return
        else:
            self.old_theme = self.theme
            self.old_primary = self.primary
            self.old_hue = self.hue
    
    def check_changes(self):
        if self.theme == self.old_theme and self.primary == self.old_primary and self.hue == self.old_hue:
            self.goto_screen('main', 'down')
        else:
            self.show_dialog("Not Saved", "You have not saved your settings", [["Cancel", self.revert_settings],["Save", self.apply_close]])
    def goto_screen(self, screen, side='left'):
        self.manager.set_current(screen, side)
    pass