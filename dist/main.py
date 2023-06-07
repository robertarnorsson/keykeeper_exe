# Kivy imports
from kivymd.app import MDApp
from kivy.core.window import Window

# Remove multi click
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Other imports
from pyautogui import size
import os

# Py file imports
from utils import logout
from root import Root
from constants import PROJECT_DIR

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Key Keeper"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        
        # Window size and pos
        self.sizex = 1280
        self.sizey = 720
        Window.size = (self.sizex, self.sizey)
        Window.left = (size()[0] - self.sizex)/2
        Window.top = (size()[1] - self.sizey)/2

        # Color & Themes
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        #self.theme_cls.material_style = "M3"

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.25

        # Check if the database folder exists. If not then make one else continue
        if os.path.exists(f'{PROJECT_DIR}\\database'):
            pass
        else:
            os.mkdir(f'{PROJECT_DIR}\\database')
    
    def open_settings(self, *largs):
        pass

    def on_stop(self):
        logout()
        return super().on_stop()

    def build(self):
        self.root = Root(self)
        self.root.set_current("login")

if __name__ == "__main__":
    MainApp().run()
