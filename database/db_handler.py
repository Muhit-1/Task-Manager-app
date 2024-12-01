import sqlite3
from datetime import datetime


class DatabaseHandler:
    def __init__(self, db_name="database/database.db"):
        self.db_name = db_name
        self.create_tables()

    def create_connection(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Create the necessary tables: users, tasks, and history."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()

                # Create Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                ''')

                # Create Tasks table with the notify_date_time column
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        description TEXT NOT NULL,
                        task_date TEXT NOT NULL,
                        task_time TEXT NOT NULL,
                        notify_date_time TEXT, -- New column for notifications
                        status TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')

                # Create History table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS history (
                        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        description TEXT NOT NULL,
                        task_date TEXT NOT NULL,
                        task_time TEXT NOT NULL,
                        completion_date TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')

                # Check and add `notify_date_time` column if it doesn't exist
                cursor.execute("PRAGMA table_info(tasks)")
                columns = [column[1] for column in cursor.fetchall()]
                if 'notify_date_time' not in columns:
                    cursor.execute("ALTER TABLE tasks ADD COLUMN notify_date_time TEXT")

                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    # User Management Methods
    def register_user(self, username, password):
        """Register a new user."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, password)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error registering user: {e}")

    def validate_user(self, username, password):
        """Validate user credentials."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id FROM users WHERE username = ? AND password = ?',
                    (username, password)
                )
                result = cursor.fetchone()
                return result[0] if result else None  # Return user ID if valid, else None
        except sqlite3.Error as e:
            print(f"Error validating user: {e}")
        return None

    # Task Management Methods
    def get_user_tasks(self, user_id):
        """Retrieve all tasks for a given user."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM tasks WHERE user_id = ?',
                    (user_id,)
                )
                return cursor.fetchall()  # Returns a list of tasks
        except sqlite3.Error as e:
            print(f"Error fetching tasks: {e}")
            return []

    def add_task_with_notification(self, user_id, description, task_date, task_time):
        """
        Add a new task and automatically set the notify_date_time
        based on the given task_date and task_time.
        """
        try:
            # Combine task_date and task_time into notify_date_time
            notify_date_time = f"{task_date} {task_time}"
            notify_date_time = datetime.strptime(notify_date_time, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

            # Validate the combined datetime format
            datetime.strptime(notify_date_time, "%Y-%m-%d %H:%M")

            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (user_id, description, task_date, task_time, notify_date_time, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, description, task_date, task_time, notify_date_time, 'Pending'))
                conn.commit()
                print("Task with notification added successfully.")
        except ValueError:
            print("Error: Invalid date or time format. Please use 'YYYY-MM-DD' for date and 'HH:MM' for time.")
        except sqlite3.Error as e:
            print(f"Error adding task with notification: {e}")

    def add_task(self, user_id, description, task_date, task_time):
        """
        Add a new task and delegate to `add_task_with_notification` for consistent behavior.
        """
        self.add_task_with_notification(user_id, description, task_date, task_time)

    def edit_task(self, task_id, description, task_date, task_time):
        """Edit an existing task."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tasks 
                    SET description = ?, task_date = ?, task_time = ? 
                    WHERE task_id = ?
                ''', (description, task_date, task_time, task_id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error editing task: {e}")

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'DELETE FROM tasks WHERE task_id = ?',
                    (task_id,)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")

    def mark_task_done(self, task_id):
        """Mark a task as completed and move it to the history table."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()

                # Retrieve the task
                cursor.execute('''
                    SELECT user_id, description, task_date, task_time 
                    FROM tasks WHERE task_id = ?
                ''', (task_id,))
                task = cursor.fetchone()

                if task:
                    user_id, description, task_date, task_time = task

                    # Insert into history
                    cursor.execute('''
                        INSERT INTO history (user_id, description, task_date, task_time, completion_date)
                        VALUES (?, ?, ?, ?, DATE('now'))
                    ''', (user_id, description, task_date, task_time))

                    # Delete the task
                    cursor.execute(
                        'DELETE FROM tasks WHERE task_id = ?',
                        (task_id,)
                    )

                conn.commit()
        except sqlite3.Error as e:
            print(f"Error marking task as done: {e}")

    # Notification Management
    def fetch_due_notifications(self):
        """Fetch tasks with notifications that are due now."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                query = '''
                    SELECT task_id, description, notify_date_time
                    FROM tasks
                    WHERE notify_date_time <= ? AND status = 'Pending'
                '''
                cursor.execute(query, (current_time,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching due notifications: {e}")
            return []

    def mark_task_as_notified(self, task_id):
        """Mark a task as notified by clearing the notify_date_time field."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = '''
                    UPDATE tasks
                    SET notify_date_time = NULL
                    WHERE task_id = ?
                '''
                cursor.execute(query, (task_id,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error marking task as notified: {e}")

    # History Management Methods
    def get_completed_tasks(self, user_id):
        """Fetch all completed tasks for a user from the history table."""
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                query = '''
                    SELECT * FROM history WHERE user_id = ?
                '''
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching completed tasks: {e}")
            return []
