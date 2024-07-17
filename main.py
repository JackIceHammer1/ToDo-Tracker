import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from datetime import datetime, timedelta

# Global variable to store user data (for demonstration purposes)
users = {
    'user1': {
        'tasks': []
    }
}

def save_data_to_file():
    # For demonstration purposes, saving data to a file would typically be done here.
    pass

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.current_user = 'user1'  # Default user for demonstration

        # Initial UI setup
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login_user).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register_user).grid(row=2, column=0, columnspan=2, pady=10)

    def login_user(self):
        username = self.username_entry.get()
        if username in users:
            self.current_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username. Please try again.")

    def register_user(self):
        username = self.username_entry.get()
        if username not in users:
            users[username] = {'tasks': []}
            self.current_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Registration Failed", "Username already exists. Please try a different username.")

    def create_main_screen(self):
        self.clear_screen()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text=f"Welcome, {self.current_user}!").grid(row=0, column=0, columnspan=6)

        tk.Button(self.main_frame, text="Add Task", command=self.create_add_task_screen).grid(row=1, column=0, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="List Tasks", command=self.list_tasks).grid(row=1, column=3, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="Search Tasks", command=self.create_search_screen).grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="Upcoming Tasks", command=self.show_upcoming_tasks).grid(row=2, column=3, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="Export Tasks", command=self.export_tasks).grid(row=3, column=0, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="Import Tasks", command=self.import_tasks).grid(row=3, column=3, columnspan=3, pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.logout_user).grid(row=4, column=0, columnspan=6, pady=10)

    def create_add_task_screen(self):
        self.clear_screen()

        self.add_task_frame = tk.Frame(self.root)
        self.add_task_frame.pack(pady=20)

        tk.Label(self.add_task_frame, text="Task Description:").grid(row=0, column=0)
        self.task_description_entry = tk.Entry(self.add_task_frame)
        self.task_description_entry.grid(row=0, column=1)

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
        description = self.task_description_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()
        recurring_days = self.recurring_entry.get()

        if description and due_date:
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
            messagebox.showerror("Error", "Please enter task description and due date")

    def list_tasks(self):
        self.clear_screen()

        self.list_tasks_frame = tk.Frame(self.root)
        self.list_tasks_frame.pack(pady=20)

        tasks = users[self.current_user]['tasks']

        if tasks:
            for idx, task in enumerate(tasks):
                row_idx = idx + 1
                tk.Label(self.list_tasks_frame, text=f"ID: {task['id']}").grid(row=row_idx, column=0)
                tk.Label(self.list_tasks_frame, text=f"Description: {task['description']}").grid(row=row_idx, column=1)
                tk.Label(self.list_tasks_frame, text=f"Priority: {task['priority']}").grid(row=row_idx, column=2)
                tk.Label(self.list_tasks_frame, text=f"Due Date: {task['due_date']}").grid(row=row_idx, column=3)
                tk.Label(self.list_tasks_frame, text=f"Category: {task['category']}").grid(row=row_idx, column=4)
                tk.Label(self.list_tasks_frame, text=f"Status: {task['status']}").grid(row=row_idx, column=5)
                tk.Label(self.list_tasks_frame, text=f"Recurring: {task['recurring_days']} days").grid(row=row_idx, column=6)

                # Buttons
                tk.Button(self.list_tasks_frame, text="Complete", command=lambda task_id=task['id']: self.complete_task(task['id'])).grid(row=row_idx, column=7)
                tk.Button(self.list_tasks_frame, text="Edit", command=lambda task_id=task['id']: self.create_edit_task_screen(task['id'])).grid(row=row_idx, column=8)
                tk.Button(self.list_tasks_frame, text="Delete", command=lambda task_id=task['id']: self.delete_task(task['id'])).grid(row=row_idx, column=9)
                tk.Button(self.list_tasks_frame, text="Add Subtask", command=lambda task_id=task['id']: self.create_add_subtask_screen(task['id'])).grid(row=row_idx, column=10)

                # Subtasks
                for sub_idx, subtask in enumerate(task['subtasks']):
                    sub_row_idx = row_idx + sub_idx + 1
                    tk.Label(self.list_tasks_frame, text=f"  Subtask: {subtask['description']}").grid(row=sub_row_idx, column=1, columnspan=4)
                    tk.Button(self.list_tasks_frame, text="Complete", command=lambda task_id=task['id'], subtask_id=subtask['id']: self.complete_subtask(task['id'], subtask['id'])).grid(row=sub_row_idx, column=7)

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
        tk.Button(self.add_subtask_frame, text="Back", command=self.create_main_screen).grid(row=2, column=0, columnspan=2, pady=10)

    def add_subtask(self, task_id):
        subtask_description = self.subtask_description_entry.get()

        if subtask_description:
            subtask = {
                'id': len(users[self.current_user]['tasks'][task_id - 1]['subtasks']) + 1,
                'description': subtask_description,
                'status': 'pending'
            }
            users[self.current_user]['tasks'][task_id - 1]['subtasks'].append(subtask)
            save_data_to_file()
            messagebox.showinfo("Success", "Subtask added successfully!")
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Please enter subtask description")

    def complete_task(self, task_id):
        users[self.current_user]['tasks'][task_id - 1]['status'] = 'completed'
        save_data_to_file()
        self.create_main_screen()

    def complete_subtask(self, task_id, subtask_id):
        users[self.current_user]['tasks'][task_id - 1]['subtasks'][subtask_id - 1]['status'] = 'completed'
        save_data_to_file()
        self.create_main_screen()

    def delete_task(self, task_id):
        confirmed = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirmed:
            del users[self.current_user]['tasks'][task_id - 1]
            save_data_to_file()
            self.create_main_screen()

    def export_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Description", "Priority", "Due Date", "Category", "Status", "Recurring"])
                for task in users[self.current_user]['tasks']:
                    writer.writerow([task['id'], task['description'], task['priority'], task['due_date'], task['category'], task['status'], task['recurring_days']])
            messagebox.showinfo("Export Successful", "Tasks exported successfully!")

    def import_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                for row in reader:
                    task = {
                        'id': int(row[0]),
                        'description': row[1],
                        'priority': row[2],
                        'due_date': row[3],
                        'category': row[4],
                        'status': row[5],
                        'recurring_days': row[6],
                        'subtasks': []
                    }
                    users[self.current_user]['tasks'].append(task)
            messagebox.showinfo("Import Successful", "Tasks imported successfully!")
            self.create_main_screen()

    def create_edit_task_screen(self, task_id):
        self.clear_screen()

        task = users[self.current_user]['tasks'][task_id - 1]

        self.edit_task_frame = tk.Frame(self.root)
        self.edit_task_frame.pack(pady=20)

        tk.Label(self.edit_task_frame, text="Task Description:").grid(row=0, column=0)
        self.task_description_entry = tk.Entry(self.edit_task_frame)
        self.task_description_entry.insert(0, task['description'])
        self.task_description_entry.grid(row=0, column=1)

        tk.Label(self.edit_task_frame, text="Priority:").grid(row=1, column=0)
        self.priority_var = tk.StringVar(value=task['priority'])
        tk.OptionMenu(self.edit_task_frame, self.priority_var, "low", "medium", "high").grid(row=1, column=1)

        tk.Label(self.edit_task_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.due_date_entry = tk.Entry(self.edit_task_frame)
        self.due_date_entry.insert(0, task['due_date'])
        self.due_date_entry.grid(row=2, column=1)

        tk.Label(self.edit_task_frame, text="Category:").grid(row=3, column=0)
        self.category_entry = tk.Entry(self.edit_task_frame)
        self.category_entry.insert(0, task['category'])
        self.category_entry.grid(row=3, column=1)

        tk.Label(self.edit_task_frame, text="Recurring (days):").grid(row=4, column=0)
        self.recurring_entry = tk.Entry(self.edit_task_frame)
        self.recurring_entry.insert(0, task['recurring_days'])
        self.recurring_entry.grid(row=4, column=1)

        tk.Button(self.edit_task_frame, text="Update Task", command=lambda: self.update_task(task_id)).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.edit_task_frame, text="Back", command=self.create_main_screen).grid(row=6, column=0, columnspan=2, pady=10)

    def update_task(self, task_id):
        task = users[self.current_user]['tasks'][task_id - 1]
        task['description'] = self.task_description_entry.get()
        task['priority'] = self.priority_var.get()
        task['due_date'] = self.due_date_entry.get()
        task['category'] = self.category_entry.get()
        task['recurring_days'] = self.recurring_entry.get()

        save_data_to_file()
        messagebox.showinfo("Success", "Task updated successfully!")
        self.create_main_screen()

    def create_search_screen(self):
        self.clear_screen()

        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=20)

        tk.Label(self.search_frame, text="Search by:").grid(row=0, column=0)
        search_var = tk.StringVar()
        search_options = ttk.Combobox(self.search_frame, textvariable=search_var, values=["description", "category", "priority"])
        search_options.grid(row=0, column=1)

        tk.Label(self.search_frame, text="Keyword:").grid(row=1, column=0)
        self.keyword_entry = tk.Entry(self.search_frame)
        self.keyword_entry.grid(row=1, column=1)

        tk.Button(self.search_frame, text="Search", command=self.perform_search).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.search_frame, text="Back", command=self.create_main_screen).grid(row=3, column=0, columnspan=2, pady=10)

    def perform_search(self):
        search_by = search_options.get()
        keyword = self.keyword_entry.get().lower()
        results = []

        for task in users[self.current_user]['tasks']:
            if keyword in task[search_by].lower():
                results.append(task)

        if results:
            self.display_search_results(results)
        else:
            messagebox.showinfo("No Results", "No tasks found matching the search criteria.")

    def display_search_results(self, results):
        self.clear_screen()

        self.search_results_frame = tk.Frame(self.root)
        self.search_results_frame.pack(pady=20)

        tk.Label(self.search_results_frame, text=f"Search Results:").grid(row=0, column=0, columnspan=8)

        for idx, task in enumerate(results):
            row_idx = idx + 1
            tk.Label(self.search_results_frame, text=f"ID: {task['id']}").grid(row=row_idx, column=0)
            tk.Label(self.search_results_frame, text=f"Description: {task['description']}").grid(row=row_idx, column=1)
            tk.Label(self.search_results_frame, text=f"Priority: {task['priority']}").grid(row=row_idx, column=2)
            tk.Label(self.search_results_frame, text=f"Due Date: {task['due_date']}").grid(row=row_idx, column=3)
            tk.Label(self.search_results_frame, text=f"Category: {task['category']}").grid(row=row_idx, column=4)
            tk.Label(self.search_results_frame, text=f"Status: {task['status']}").grid(row=row_idx, column=5)
            tk.Label(self.search_results_frame, text=f"Recurring: {task['recurring_days']} days").grid(row=row_idx, column=6)

            # Buttons
            tk.Button(self.search_results_frame, text="Complete", command=lambda task_id=task['id']: self.complete_task(task_id)).grid(row=row_idx, column=7)
            tk.Button(self.search_results_frame, text="Edit", command=lambda task_id=task['id']: self.create_edit_task_screen(task_id)).grid(row=row_idx, column=8)
            tk.Button(self.search_results_frame, text="Delete", command=lambda task_id=task['id']: self.delete_task(task_id)).grid(row=row_idx, column=9)
            tk.Button(self.search_results_frame, text="Add Subtask", command=lambda task_id=task['id']: self.create_add_subtask_screen(task_id)).grid(row=row_idx, column=10)

            # Subtasks
            for sub_idx, subtask in enumerate(task['subtasks']):
                sub_row_idx = row_idx + sub_idx + 1
                tk.Label(self.search_results_frame, text=f"  Subtask: {subtask['description']}").grid(row=sub_row_idx, column=1, columnspan=4)
                tk.Button(self.search_results_frame, text="Complete", command=lambda task_id=task['id'], subtask_id=subtask['id']: self.complete_subtask(task['id'], subtask['id'])).grid(row=sub_row_idx, column=7)

        tk.Button(self.search_results_frame, text="Back", command=self.create_main_screen).grid(row=len(results)+1, column=0, columnspan=6, pady=10)

    def show_upcoming_tasks(self):
        self.clear_screen()

        self.upcoming_tasks_frame = tk.Frame(self.root)
        self.upcoming_tasks_frame.pack(pady=20)

        upcoming_tasks = [task for task in users[self.current_user]['tasks'] if task['status'] != 'completed' and self.calculate_days_until_due(task['due_date']) <= 7]

        if upcoming_tasks:
            for idx, task in enumerate(upcoming_tasks):
                row_idx = idx + 1
                tk.Label(self.upcoming_tasks_frame, text=f"ID: {task['id']}").grid(row=row_idx, column=0)
                tk.Label(self.upcoming_tasks_frame, text=f"Description: {task['description']}").grid(row=row_idx, column=1)
                tk.Label(self.upcoming_tasks_frame, text=f"Priority: {task['priority']}").grid(row=row_idx, column=2)
                tk.Label(self.upcoming_tasks_frame, text=f"Due Date: {task['due_date']}").grid(row=row_idx, column=3)
                tk.Label(self.upcoming_tasks_frame, text=f"Category: {task['category']}").grid(row=row_idx, column=4)
                tk.Label(self.upcoming_tasks_frame, text=f"Status: {task['status']}").grid(row=row_idx, column=5)
                tk.Label(self.upcoming_tasks_frame, text=f"Recurring: {task['recurring_days']} days").grid(row=row_idx, column=6)

        else:
            tk.Label(self.upcoming_tasks_frame, text="No upcoming tasks found").grid(row=1, column=0, columnspan=6)

        tk.Button(self.upcoming_tasks_frame, text="Back", command=self.create_main_screen).grid(row=len(upcoming_tasks)+2, column=0, columnspan=6, pady=10)

    def calculate_days_until_due(self, due_date_str):
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            today = datetime.now()
            return (due_date - today).days
        return None

    def logout_user(self):
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("To-Do List Tracker")
    root.geometry("800x600")

    app = TodoApp(root)

    root.mainloop()
