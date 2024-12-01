from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDTimePicker  # Import Date and Time Picker
from kivy.uix.textinput import TextInput
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel

from database.db_handler import DatabaseHandler

db_handler = DatabaseHandler()


class TaskPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.selected_date = None
        self.selected_time = None

    def on_enter(self):
        if self.user_id:
            self.update_task_list()

    def show_task_popup(self):
        popup_layout = BoxLayout(orientation="vertical", spacing=15, padding=10)

        task_desc = TextInput(hint_text="Enter task description", multiline=False)

        # Replace date and time text inputs with buttons
        date_btn = Button(text="Select Date", size_hint_y=None, height=50)
        time_btn = Button(text="Select Time", size_hint_y=None, height=50)

        # Bind buttons to open pickers
        date_btn.bind(on_release=self.show_date_picker)
        time_btn.bind(on_release=self.show_time_picker)

        popup_layout.add_widget(task_desc)
        popup_layout.add_widget(date_btn)
        popup_layout.add_widget(time_btn)

        buttons = BoxLayout(orientation="horizontal", spacing=10)
        add_btn = MDRaisedButton(text="Add", md_bg_color=(0.2, 0.5, 0.8, 1))
        close_btn = MDRaisedButton(text="Close", md_bg_color=(0.86, 0.2, 0.2, 1))
        buttons.add_widget(add_btn)
        buttons.add_widget(close_btn)

        popup_layout.add_widget(buttons)

        popup = Popup(title="Add Task", content=popup_layout, size_hint=(0.8, 0.5))

        # Bind Add button to add_task function
        add_btn.bind(on_release=lambda *args: self.add_task(task_desc.text, popup))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def show_date_picker(self, *args):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance, value, date_range):
        self.selected_date = str(value)

    def show_time_picker(self, *args):
        time_picker = MDTimePicker()
        time_picker.bind(time=self.on_time_selected)
        time_picker.open()

    def on_time_selected(self, instance, time):
        self.selected_time = time.strftime("%H:%M")

    def add_task(self, description, popup):
        if description and self.selected_date and self.selected_time:
            db_handler.add_task(self.user_id, description, self.selected_date, self.selected_time)
            self.update_task_list()
            popup.dismiss()
        else:
            popup.content.add_widget(Label(text="All fields are required!", color=(1, 0, 0, 1)))

    def update_task_list(self):
        tasks = db_handler.get_user_tasks(self.user_id)
        task_list = self.ids.task_list
        task_list.clear_widgets()

        for task in tasks:
            task_widget = TaskWidget(task, self)
            task_widget.size_hint_y = None
            task_widget.height = dp(140)
            task_list.add_widget(task_widget)

        task_list.height = len(task_list.children) * dp(150)  # Adjusting for task height + spacing

    def mark_task_done(self, task_id):
        db_handler.mark_task_done(task_id)
        self.update_task_list()

    def edit_task(self, task_id, new_desc, new_date, new_time):
        db_handler.edit_task(task_id, new_desc, new_date, new_time)
        self.update_task_list()

    def delete_task(self, task_id):
        db_handler.delete_task(task_id)
        self.update_task_list()

    def show_snackbar(self, message):
        Snackbar(text=message, duration=3).open()

    def show_completed_tasks_popup(self):
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        completed_tasks = db_handler.get_completed_tasks(self.user_id)

        if not completed_tasks:
            popup_layout.add_widget(Label(text="No completed tasks."))
        else:
            for task in completed_tasks:
                popup_layout.add_widget(Label(text=f"{task[2]} - {task[3]} {task[4]}"))

        close_btn = Button(text="Close", size_hint=(1, 0.2))
        popup_layout.add_widget(close_btn)

        popup = Popup(title="Completed Tasks", content=popup_layout, size_hint=(0.8, 0.6))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class TaskWidget(MDCard):
    def __init__(self, task, task_page, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.task_page = task_page
        self.orientation = "vertical"  # Vertical layout for content
        self.padding = dp(10)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(140)  # Increased height for better spacing
        self.md_bg_color = (1, 1, 1, 1)

        # Container for the description, date, and time
        content_layout = BoxLayout(orientation="vertical", spacing=dp(5))

        # Task description
        task_desc = Label(
            text=f"[b]{task[2]}[/b]",  # Bold text using markup
            markup=True,
            color=(0, 0, 0, 1),  # Black font
            size_hint_y=None,
            height=dp(40),
        )
        content_layout.add_widget(task_desc)

        # Task date and time
        task_datetime = Label(
            text=f"{task[3]} {task[4]}",  # Date and time
            color=(0, 0, 0, 1),  # Black font
            size_hint_y=None,
            height=dp(20),
        )
        content_layout.add_widget(task_datetime)

        self.add_widget(content_layout)

        # Buttons container
        buttons_layout = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(40))

        # Done button
        done_btn = Button(
            text="Done",
            size_hint_x=0.3,
            background_color=(0.2, 0.7, 0.3, 1),
        )
        done_btn.bind(on_release=lambda *args: self.task_page.mark_task_done(self.task[0]))
        buttons_layout.add_widget(done_btn)

        # Edit button
        edit_btn = Button(
            text="Edit",
            size_hint_x=0.3,
            background_color=(0.9, 0.6, 0.2, 1),
        )
        edit_btn.bind(on_release=lambda instance: self.show_edit_popup())
        buttons_layout.add_widget(edit_btn)

        # Delete button
        delete_btn = Button(
            text="Delete",
            size_hint_x=0.3,
            background_color=(0.8, 0.2, 0.2, 1),
        )
        delete_btn.bind(on_release=lambda *args: self.task_page.delete_task(self.task[0]))
        buttons_layout.add_widget(delete_btn)

        self.add_widget(buttons_layout)

    def show_edit_popup(self):
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        desc_input = TextInput(text=self.task[2], multiline=False)
        date_input = TextInput(text=self.task[3], multiline=False)
        time_input = TextInput(text=self.task[4], multiline=False)

        popup_layout.add_widget(desc_input)
        popup_layout.add_widget(date_input)
        popup_layout.add_widget(time_input)

        buttons = BoxLayout(orientation="horizontal", spacing=10)
        save_btn = Button(text="Save")
        close_btn = Button(text="Close")
        buttons.add_widget(save_btn)
        buttons.add_widget(close_btn)

        popup_layout.add_widget(buttons)

        popup = Popup(title="Edit Task", content=popup_layout, size_hint=(0.8, 0.5))
        save_btn.bind(on_release=lambda *args: self.task_page.edit_task(
            self.task[0], desc_input.text, date_input.text, time_input.text))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
