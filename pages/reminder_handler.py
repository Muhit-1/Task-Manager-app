from datetime import datetime
from plyer import notification
from playsound import playsound
import threading

class ReminderHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.sound_file = "notification_sound.mp3"  # Path to your sound file

    def check_reminders(self, *args):
        """Check for due reminders and send notifications."""
        due_reminders = self.db_handler.fetch_due_notifications()
        for reminder in due_reminders:
            task_id, description, notify_time = reminder
            # Trigger notification
            self.send_notification(description)
            # Play sound in a separate thread
            threading.Thread(target=self.play_sound).start()
            # Mark task as notified
            self.db_handler.mark_task_as_notified(task_id)

    def send_notification(self, message):
        """Send a desktop notification."""
        notification.notify(
            title="Task Reminder",
            message=message,
            app_name="To-Do List",
            timeout=10  # Seconds
        )

    def play_sound(self):
        """Play notification sound."""
        try:
            playsound(self.sound_file)
        except Exception as e:
            print(f"Error playing sound: {e}")
