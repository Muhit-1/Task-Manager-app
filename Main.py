from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock  # For scheduling periodic tasks
from kivymd.app import MDApp
from database.db_handler import DatabaseHandler
from pages.reminder_handler import ReminderHandler  # Your new ReminderHandler module
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.task_page import TaskPage

# Load KV files for the screens
Builder.load_file("kv file/login_page.kv")
Builder.load_file("kv file/register_page.kv")
Builder.load_file("kv file/task_page.kv")


class MainApp(MDApp):
    def build(self):
        # Initialize the database handler
        self.db_handler = DatabaseHandler()

        # Initialize the ReminderHandler
        self.reminder_handler = ReminderHandler(self.db_handler)

        # Schedule periodic reminder checks every 60 seconds
        Clock.schedule_interval(self.reminder_handler.check_reminders, 30)

        # Set up the screen manager
        sm = ScreenManager()
        sm.add_widget(LoginPage(name="login"))
        sm.add_widget(RegisterPage(name="register"))
        sm.add_widget(TaskPage(name="task"))
        return sm


if __name__ == "__main__":
    MainApp().run()

