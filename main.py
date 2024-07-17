import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime, timedelta
import csv
import hashlib

# Initialize a dictionary to store tasks and user information
users = {}

def save_data_to_file(filename='tasks.json'):
    """Save users and tasks to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)

def load_data_from_file(filename='tasks.json'):
    """Load users and tasks from a JSON file."""
    global users
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

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

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login_user).grid(row=2, column=0, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.create_registration_screen).grid(row=2, column=1, pady=10)

    def create_registration_screen(self):
        self.clear_screen()

        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack(pady=20)

        tk.Label(self.registration_frame, text="Username:").grid(row=0, column=0)
        self.reg_username_entry = tk.Entry(self.registration_frame)
        self.reg_username_entry.grid(row=0, column=1)

        tk.Label(self.registration_frame, text="Password:").grid(row=1, column=0)
        self.reg_password_entry = tk.Entry(self.registration_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1)

        tk.Button(self.registration_frame, text="Register", command=self.register_user).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.registration_frame, text="Back", command=self.create_login_screen).grid(row=3, column=0, columnspan=2, pady=10)

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if username and password:
            if username in users:
                messagebox.showerror("Error", "Username already exists")
            else:
                users[username] = {
                    'password': hash_password(password),
                    'tasks': []
                }
                save_data_to_file()
                messagebox.showinfo("Success", "User registered successfully!")
                self.create_login_screen()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username]['password'] == hash_password(password):
            self.current_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

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

        tk.Label(self.add_task_frame, text="Recurring (days):").grid(row=4, column=0)
        self.recurring_entry = tk.Entry(self.add_task_frame)
        self.recurring_entry.grid(row=4, column=1)

        tk.Button(self.add_task_frame, text="Add Task", command=self.add_task).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.add_task_frame, text="Back", command=self.create_main_screen).grid(row=6, column=0, columnspan=2, pady=10)

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()
        recurring_days = self.recurring_entry.get()

        if description:
            task = {
                'id': len(users[self.current_user]['tasks']) + 1,
                'description': description,
                'priority': priority,
                'due_date': due_date,
                'category': category,
                'status': 'pending',
                'recurring_days': recurring_days,
                'subtasks': []
            }
            users[self.current_user]['tasks'].append(task)
            save_data_to_file()
            messagebox.showinfo("Success", "Task added successfully!")
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Please enter a task description")

    def list_tasks(self):
        self.clear_screen()

        self.list_tasks_frame = tk.Frame(self.root)
        self.list_tasks_frame.pack(pady=20)

        tk.Label(self.list_tasks_frame, text=f"Tasks for {self.current_user}:").grid(row=0, column=0, columnspan=6)

        tasks = users[self.current_user]['tasks']

        if tasks:
            for idx, task in enumerate(tasks):
                tk.Label(self.list_tasks_frame, text=f"ID: {task['id']}").grid(row=idx+1, column=0)
                tk.Label(self.list_tasks_frame, text=f"Description: {task['description']}").grid(row=idx+1, column=1)
                tk.Label(self.list_tasks_frame, text=f"Priority: {task['priority']}").grid(row=idx+1, column=2)
                tk.Label(self.list_tasks_frame, text=f"Due Date: {task['due_date']}").grid(row=idx+1, column=3)
                tk.Label(self.list_tasks_frame, text=f"Category: {task['category']}").grid(row=idx+1, column=4)
                tk.Label(self.list_tasks_frame, text=f"Status: {task['status']}").grid(row=idx+1, column=5)
                tk.Label(self.list_tasks_frame, text=f"Recurring: {task['recurring_days']} days").grid(row=idx+1, column=6)
                tk.Button(self.list_tasks_frame, text="Complete", command=lambda task_id=task['id']: self.complete_task(task_id)).grid(row=idx+1, column=7)
                tk.Button(self.list_tasks_frame, text="Edit", command=lambda task_id=task['id']: self.create_edit_task_screen(task_id)).grid(row=idx+1, column=8)
                tk.Button(self.list_tasks_frame, text="Delete", command=lambda task_id=task['id']: self.delete_task(task_id)).grid(row=idx+1, column=9)
                tk.Button(self.list_tasks_frame, text="Add Subtask", command=lambda task_id=task['id']: self.create_add_subtask_screen(task_id)).grid(row=idx+1, column=10)

                for sub_idx, subtask in enumerate(task['subtasks']):
                    tk.Label(self.list_tasks_frame, text=f"  Subtask: {subtask['description']}").grid(row=idx+sub_idx+2, column=1, columnspan=4)
                    tk.Button(self.list_tasks_frame, text="Complete", command=lambda task_id=task['id'], subtask_id=subtask['id']: self.complete_subtask(task_id, subtask_id)).grid(row=idx+sub_idx+2, column=7)
        else:
            tk.Label(self.list_tasks_frame, text="No tasks found").grid(row=1, column=0, columnspan=6)

        tk.Button(self.list_tasks_frame, text="Back", command=self.create_main_screen).grid(row=len(tasks)+2, column=0, columnspan=6, pady=10)

    def create_add_subtask_screen(self, task_id):
        self.clear_screen()

        self.add_subtask_frame = tk.Frame(self.root)
        self.add_subtask_frame.pack(pady=20)

        tk.Label(self.add_subtask_frame, text="Subtask Description:").grid(row=0, column=0)
        self.subtask_description_entry = tk.Entry(self.add_subtask_frame)
        self.subtask_description_entry.grid(row=0, column=1)

        tk.Button(self.add_subtask_frame, text="Add Subtask", command=lambda: self.add_subtask(task_id)).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.add_subtask_frame, text="Back", command=self.list_tasks).grid(row=2, column=0, columnspan=2, pady=10)

    def add_subtask(self, task_id):
        description = self.subtask_description_entry.get()

        if description:
            for task in users[self.current_user]['tasks']:
                if task['id'] == task_id:
                    subtask = {
                        'id': len(task['subtasks']) + 1,
                        'description': description,
                        'status': 'pending'
                    }
                    task['subtasks'].append(subtask)
                    save_data_to_file()
                    messagebox.showinfo("Success", "Subtask added successfully!")
                    self.list_tasks()
                    return
        else:
            messagebox.showerror("Error", "Please enter a subtask description")

    def complete_subtask(self, task_id, subtask_id):
        for task in users[self.current_user]['tasks']:
            if task['id'] == task_id:
                for subtask in task['subtasks']:
                    if subtask['id'] == subtask_id:
                        subtask['status'] = 'complete'
                        save_data_to_file()
                        messagebox.showinfo("Success", f"Subtask ID {subtask_id} completed.")
                        self.list_tasks()
                        return
        messagebox.showerror("Error", f"Subtask ID {subtask_id} not found.")

    def complete_task(self, task_id):
        for task in users[self.current_user]['tasks']:
            if task['id'] == task_id:
                task['status'] = 'complete'
                self.handle_recurring_task(task)
                save_data_to_file()
                messagebox.showinfo("Success", f"Task ID {task_id} completed.")
                self.list_tasks()
                return
        messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def handle_recurring_task(self, task):
        if task['recurring_days']:
            recurring_days = int(task['recurring_days'])
            new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(days=recurring_days)).strftime("%Y-%m-%d")
            new_task = task.copy()
            new_task['id'] = len(users[self.current_user]['tasks']) + 1
            new_task['due_date'] = new_due_date
            new_task['status'] = 'pending'
            users[self.current_user]['tasks'].append(new_task)

    def create_edit_task_screen(self, task_id):
        self.clear_screen()

        self.edit_task_frame = tk.Frame(self.root)
        self.edit_task_frame.pack(pady=20)

        for task in users[self.current_user]['tasks']:
            if task['id'] == task_id:
                self.current_task = task
                break

        tk.Label(self.edit_task_frame, text="Description:").grid(row=0, column=0)
        self.edit_description_entry = tk.Entry(self.edit_task_frame)
        self.edit_description_entry.insert(0, self.current_task['description'])
        self.edit_description_entry.grid(row=0, column=1)

        tk.Label(self.edit_task_frame, text="Priority:").grid(row=1, column=0)
        self.edit_priority_var = tk.StringVar(value=self.current_task['priority'])
        tk.OptionMenu(self.edit_task_frame, self.edit_priority_var, "low", "medium", "high").grid(row=1, column=1)

        tk.Label(self.edit_task_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.edit_due_date_entry = tk.Entry(self.edit_task_frame)
        self.edit_due_date_entry.insert(0, self.current_task['due_date'])
        self.edit_due_date_entry.grid(row=2, column=1)

        tk.Label(self.edit_task_frame, text="Category:").grid(row=3, column=0)
        self.edit_category_entry = tk.Entry(self.edit_task_frame)
        self.edit_category_entry.insert(0, self.current_task['category'])
        self.edit_category_entry.grid(row=3, column=1)

        tk.Label(self.edit_task_frame, text="Recurring (days):").grid(row=4, column=0)
        self.edit_recurring_entry = tk.Entry(self.edit_task_frame)
        self.edit_recurring_entry.insert(0, self.current_task['recurring_days'])
        self.edit_recurring_entry.grid(row=4, column=1)

        tk.Button(self.edit_task_frame, text="Update Task", command=self.update_task).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.edit_task_frame, text="Back", command=self.list_tasks).grid(row=6, column=0, columnspan=2, pady=10)

    def update_task(self):
        self.current_task['description'] = self.edit_description_entry.get()
        self.current_task['priority'] = self.edit_priority_var.get()
        self.current_task['due_date'] = self.edit_due_date_entry.get()
        self.current_task['category'] = self.edit_category_entry.get()
        self.current_task['recurring_days'] = self.edit_recurring_entry.get()
        save_data_to_file()
        messagebox.showinfo("Success", "Task updated successfully!")
        self.list_tasks()

    def delete_task(self, task_id):
        for task in users[self.current_user]['tasks']:
            if task['id'] == task_id:
                users[self.current_user]['tasks'].remove(task)
                save_data_to_file()
                messagebox.showinfo("Success", f"Task ID {task_id} deleted.")
                self.list_tasks()
                return
        messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def export_tasks(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['id', 'description', 'priority', 'due_date', 'category', 'status', 'recurring_days']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for task in users[self.current_user]['tasks']:
                    writer.writerow(task)
            messagebox.showinfo("Success", f"Tasks exported to {filename}")

    def import_tasks(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task = {
                        'id': len(users[self.current_user]['tasks']) + 1,
                        'description': row['description'],
                        'priority': row['priority'],
                        'due_date': row['due_date'],
                        'category': row['category'],
                        'status': row['status'],
                        'recurring_days': row['recurring_days'],
                        'subtasks': []
                    }
                    users[self.current_user]['tasks'].append(task)
            save_data_to_file()
            messagebox.showinfo("Success", f"Tasks imported from {filename}")
            self.list_tasks()

    def logout_user(self):
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    load_data_from_file()  # Load tasks from file on startup

    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
