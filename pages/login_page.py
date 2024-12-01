from kivy.uix.screenmanager import Screen
from database.db_handler import DatabaseHandler


class LoginPage(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        # Create a database handler instance
        db_handler = DatabaseHandler()

        # Validate user credentials
        user_id = db_handler.validate_user(username, password)

        if user_id:
            print(f"Login successful! User ID: {user_id}")
            self.manager.current = 'task'  # Navigate to the Task Page
            self.manager.get_screen('task').user_id = user_id  # Pass the user ID
        else:
            print("Invalid username or password")
