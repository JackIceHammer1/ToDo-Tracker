import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from datetime import datetime
import csv

# Initialize a dictionary to store tasks for different users
users = {}

def save_tasks_to_file(filename='tasks.json'):
    """Save tasks to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)

def load_tasks_from_file(filename='tasks.json'):
    """Load tasks from a JSON file."""
    global users
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}  # Start with an empty dictionary if file doesn't exist

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Tracker")

        self.current_user = None

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login_user).grid(row=1, column=0, columnspan=2, pady=10)

    def login_user(self):
        username = self.username_entry.get()
        if username:
            self.current_user = username
            if username not in users:
                users[username] = []
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Please enter a username")

    def create_main_screen(self):
        self.clear_screen()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text=f"Welcome, {self.current_user}").grid(row=0, column=0, columnspan=2)

        tk.Button(self.main_frame, text="Add Task", command=self.create_add_task_screen).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="List Tasks", command=self.list_tasks).grid(row=1, column=1, pady=5)
        tk.Button(self.main_frame, text="Export Tasks", command=self.export_tasks).grid(row=2, column=0, pady=5)
        tk.Button(self.main_frame, text="Import Tasks", command=self.import_tasks).grid(row=2, column=1, pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout_user).grid(row=3, column=0, columnspan=2, pady=10)

    def create_add_task_screen(self):
        self.clear_screen()

        self.add_task_frame = tk.Frame(self.root)
        self.add_task_frame.pack(pady=20)

        tk.Label(self.add_task_frame, text="Description:").grid(row=0, column=0)
        self.description_entry = tk.Entry(self.add_task_frame)
        self.description_entry.grid(row=0, column=1)

        tk.Label(self.add_task_frame, text="Priority:").grid(row=1, column=0)
        self.priority_var = tk.StringVar(value="low")
        tk.OptionMenu(self.add_task_frame, self.priority_var, "low", "medium", "high").grid(row=1, column=1)

        tk.Label(self.add_task_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.due_date_entry = tk.Entry(self.add_task_frame)
        self.due_date_entry.grid(row=2, column=1)

        tk.Label(self.add_task_frame, text="Category:").grid(row=3, column=0)
        self.category_entry = tk.Entry(self.add_task_frame)
        self.category_entry.grid(row=3, column=1)

        tk.Button(self.add_task_frame, text="Add Task", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.add_task_frame, text="Back", command=self.create_main_screen).grid(row=5, column=0, columnspan=2, pady=10)

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()

        if description:
            task = {
                'id': len(users[self.current_user]) + 1,
                'description': description,
                'priority': priority,
                'due_date': due_date,
                'category': category,
                'status': 'pending'
            }
            users[self.current_user].append(task)
            save_tasks_to_file()
            messagebox.showinfo("Success", "Task added successfully!")
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Please enter a task description")

    def list_tasks(self):
        self.clear_screen()

        self.list_tasks_frame = tk.Frame(self.root)
        self.list_tasks_frame.pack(pady=20)

self.delete_task(task_id)).grid(row=idx+1, column=8)
        else:
            tk.Label(self.list_tasks_frame, text="No tasks found.").grid(row=1, column=0, columnspan=4)

        tk.Button(self.list_tasks_frame, text="Back", command=self.create_main_screen).grid(row=len(tasks)+2, column=0, columnspan=4, pady=10)

    def complete_task(self, task_id):
        for task in users[self.current_user]:
            if task['id'] == task_id:
                task['status'] = 'completed'
                save_tasks_to_file()
                messagebox.showinfo("Success", f"Task ID {task_id} marked as completed.")
                self.list_tasks()
                return
        messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def create_edit_task_screen(self, task_id):
        self.clear_screen()

        self.edit_task_frame = tk.Frame(self.root)
        self.edit_task_frame.pack(pady=20)

        for task in users[self.current_user]:
            if task['id'] == task_id:
                self.current_task = task
                break
        else:
            messagebox.showerror("Error", f"Task ID {task_id} not found.")
            self.create_main_screen()
            return

if __name__ == "__main__":
    load_tasks_from_file()  # Load tasks from file on startup

    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
