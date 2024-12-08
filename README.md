Contact
Muhit Rahman
Email: [senanovi908@gmail.com]
GitHub: Muhit-1
# Task Manager App

A Python-based **Task Manager Application** built using **Kivy** and **KivyMD** for creating, managing, and tracking tasks with notification functionality. This app allows users to register, log in, add, edit, and delete tasks, with completed tasks stored in history.

---

## Features
- **User Authentication**: Login and Registration system.
- **Task Management**:
  - Add tasks with a date and time for notifications.
  - Edit or delete tasks.
  - Mark tasks as completed.
- **History Tracking**: Keeps track of completed tasks.
- **Database Integration**: Uses SQLite for data storage.
- **Cross-Platform UI**: Developed with KivyMD for a modern, responsive interface.

---

## Technology Stack
- **Programming Language**: Python
- **Frameworks**: 
  - [Kivy](https://kivy.org/)
  - [KivyMD](https://kivymd.readthedocs.io/)
- **Database**: SQLite
- **Version Control**: Git & GitHub
- **Development Environment**: PyCharm

---

Task-Manager-app/
├── database/
│   └── db_handler.py    # Handles SQLite database operations
├── kv file/
│   ├── login_page.kv    # Kivy layout for Login Page
│   ├── register_page.kv # Kivy layout for Register Page
│   ├── task_page.kv     # Kivy layout for Task Management
├── pages/
│   ├── login_page.py    # Logic for Login Page
│   ├── register_page.py # Logic for Registration Page
│   ├── task_page.py     # Logic for Task Management Page
├── main.py              # Main entry point of the application
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
└── .gitignore           # Files and folders to ignore in Git


## Prerequisites
Before you begin, ensure you have met the following requirements:
1. **Python** (3.7 or above) installed on your system.
2. Required Python packages installed:
   - Kivy
   - KivyMD
   - SQLite
   - Any other dependencies specified in the `requirements.txt` file.

To install the dependencies, run:
```bash
pip install -r requirements.txt


  
