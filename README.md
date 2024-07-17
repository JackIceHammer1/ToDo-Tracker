# To-Do List Tracker

A feature-rich to-do list application built with Python and Tkinter. This application allows users to manage their tasks effectively, including features like task addition, listing, searching, categorizing, prioritizing, recurring tasks, subtasks, importing/exporting tasks, and more.

## Features

- **User Authentication**: Simple login and registration system to manage tasks for multiple users.
- **Task Management**: Add, edit, complete, and delete tasks with various attributes like description, priority, due date, category, and recurrence.
- **Subtasks**: Manage subtasks under main tasks.
- **Search Functionality**: Search tasks by description, category, or priority.
- **Upcoming Tasks**: View tasks due in the next 7 days.
- **Import/Export**: Import tasks from and export tasks to CSV files.
- **Responsive UI**: Intuitive and responsive graphical user interface using Tkinter.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/todo-list-tracker.git
    cd todo-list-tracker
    ```

2. Install required dependencies (if any). For Tkinter, it typically comes pre-installed with Python.

3. Run the application:
    ```bash
    python todo_app.py
    ```

## Usage

1. **Login/Register**: 
   - On startup, enter a username to login or register.
   
2. **Main Screen**:
   - **Add Task**: Opens a form to add a new task.
   - **List Tasks**: Displays a list of all tasks with options to complete, edit, delete, or add subtasks.
   - **Search Tasks**: Opens a search screen to find tasks by description, category, or priority.
   - **Upcoming Tasks**: Shows tasks due in the next 7 days.
   - **Export Tasks**: Save tasks to a CSV file.
   - **Import Tasks**: Load tasks from a CSV file.
   - **Logout**: Logout and return to the login screen.

3. **Adding/Editing Tasks**:
   - Provide task details including description, priority, due date, category, and recurrence days.
   - Subtasks can be added by navigating to the main task and selecting "Add Subtask".

4. **Task Management**:
   - Complete, edit, or delete tasks directly from the task list.
   - View and manage subtasks under each main task.