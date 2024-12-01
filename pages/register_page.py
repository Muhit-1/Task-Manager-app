from kivy.uix.screenmanager import Screen
from database.db_handler import DatabaseHandler
from kivy.uix.popup import Popup
from kivy.uix.label import Label

db = DatabaseHandler()

class RegisterPage(Screen):
    def register(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if username and password:
            db.register_user(username, password)
            Popup(title="Success", content=Label(text="Registration complete"), size_hint=(0.6, 0.4)).open()
        else:
            Popup(title="Error", content=Label(text="Fields cannot be empty"), size_hint=(0.6, 0.4)).open()
