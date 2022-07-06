from kivy.lang import Builder
from kivy.uix import screenmanager
from kivymd.app import MDApp

from client import Client


class LoginScreen(screenmanager.Screen):
    name = "login"


class RegisterScreen(screenmanager.Screen):
    name = "register"


class MainScreen(screenmanager.Screen):
    pass


class SManager(screenmanager.ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, transition=screenmanager.FadeTransition())


class CrystalCVApp(MDApp):
    def build(self):
        self.client = Client(app=self)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        kv = Builder.load_file("crystalcv.kv")
        return kv

    def clear_login_screen(self):
        self.root.ids.login_username.text = ""
        self.root.ids.login_password.text = ""

    def login(self, username, password):
        self.client.login(username=username, password=password)

    def register(self, username, password):
        self.client.register(username=username, password=password)

    def register_success(self, *args, **kwargs):
        pass

    def login_success(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass




if __name__ == "__main__":
    CrystalCVApp().run()
