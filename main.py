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

        tk.Label(self.list_tasks_frame, text=f"Tasks for {self.current_user}:").grid(row=0, column=0, columnspan=4)

        tasks = users[self.current_user]

        if tasks:
            for idx, task in enumerate(tasks):
                tk.Label(self.list_tasks_frame, text=f"ID: {task['id']}").grid(row=idx+1, column=0)
                tk.Label(self.list_tasks_frame, text=f"Description: {task['description']}").grid(row=idx+1, column=1)
                tk.Label(self.list_tasks_frame, text=f"Priority: {task['priority']}").grid(row=idx+1, column=2)
                tk.Label(self.list_tasks_frame, text=f"Due Date: {task['due_date']}").grid(row=idx+1, column=3)
                tk.Label(self.list_tasks_frame, text=f"Category: {task['category']}").grid(row=idx+1, column=4)
                tk.Label(self.list_tasks_frame, text=f"Status: {task['status']}").grid(row=idx+1, column=5)
                tk.Button(self.list_tasks_frame, text="Complete", command=lambda task_id=task['id']: self.complete_task(task_id)).grid(row=idx+1, column=6)
                tk.Button(self.list_tasks_frame, text="Edit", command=lambda task_id=task['id']: self.create_edit_task_screen(task_id)).grid(row=idx+1, column=7)
                tk.Button(self.list_tasks_frame, text="Delete", command=lambda task_id=task['id']: self.delete_task(task_id)).grid(row=idx+1, column=8)
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

        tk.Button(self.edit_task_frame, text="Update Task", command=self.update_task).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.edit_task_frame, text="Back", command=self.list_tasks).grid(row=5, column=0, columnspan=2, pady=10)

    def update_task(self):
        self.current_task['description'] = self.edit_description_entry.get()
        self.current_task['priority'] = self.edit_priority_var.get()
        self.current_task['due_date'] = self.edit_due_date_entry.get()
        self.current_task['category'] = self.edit_category_entry.get()
        save_tasks_to_file()
        messagebox.showinfo("Success", "Task updated successfully!")
        self.list_tasks()

    def delete_task(self, task_id):
        for task in users[self.current_user]:
            if task['id'] == task_id:
                users[self.current_user].remove(task)
                save_tasks_to_file()
                messagebox.showinfo("Success", f"Task ID {task_id} deleted.")
                self.list_tasks()
                return
        messagebox.showerror("Error", f"Task ID {task_id} not found.")

    def export_tasks(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['id', 'description', 'priority', 'due_date', 'category', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for task in users[self.current_user]:
                    writer.writerow(task)
            messagebox.showinfo("Success", f"Tasks exported to {filename}")

    def import_tasks(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task = {
                        'id': len(users[self.current_user]) + 1,
                        'description': row['description'],
                        'priority': row['priority'],
                        'due_date': row['due_date'],
                        'category': row['category'],
                        'status': row['status']
                    }
                    users[self.current_user].append(task)
            save_tasks_to_file()
            messagebox.showinfo("Success", f"Tasks imported from {filename}")
            self.list_tasks()

    def logout_user(self):
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    load_tasks_from_file()  # Load tasks from file on startup

    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
