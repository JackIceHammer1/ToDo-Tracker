import argparse
import json
import csv
from datetime import datetime

# Initialize a dictionary to store tasks for different users
users = {}

def add_task(user, task_description, priority='low', due_date=None, category=None):
    """Add a new task to the task list for a user."""
    if user not in users:
        users[user] = []
    
    task = {
        'id': len(users[user]) + 1,
        'description': task_description,
        'priority': priority,
        'due_date': due_date,
        'category': category,
        'status': 'pending'  # Default status
    }
    users[user].append(task)
    print(f"Task added for {user}: '{task_description}'")

def list_tasks(user, filter_by=None, filter_value=None, reminders=False, sort_by=None):
    """Display all tasks in the task list for a user, with optional filtering and sorting."""
    if user not in users or not users[user]:
        print(f"No tasks found for {user}.")
        return

    tasks = users[user]

    if filter_by and filter_value:
        tasks = [task for task in tasks if task[filter_by] == filter_value]
    
    if sort_by:
        tasks = sorted(tasks, key=lambda x: x[sort_by])

    if tasks:
        print(f"Tasks for {user}:")
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Priority: {task['priority']}, Due Date: {task['due_date']}, Category: {task['category']}, Status: {task['status']}")
            if reminders:
                check_due_date(task)
    else:
        print("No tasks found.")

def check_due_date(task):
    """Check if a task's due date is approaching or overdue and print a reminder."""
    if task['due_date']:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
        days_left = (due_date - datetime.now()).days
        if days_left < 0:
            print(f"Reminder: Task ID {task['id']} is overdue!")
        elif days_left <= 3:
            print(f"Reminder: Task ID {task['id']} is due in {days_left} days.")

def mark_task_complete(user, task_id):
    """Mark a task as complete for a user."""
    if user not in users:
        print(f"No tasks found for {user}.")
        return

    for task in users[user]:
        if task['id'] == task_id:
            task['status'] = 'completed'
            print(f"Task ID {task_id} for {user} marked as completed.")
            return
    print(f"Task ID {task_id} not found for {user}.")

def edit_task(user, task_id, new_description=None, new_priority=None, new_due_date=None, new_category=None):
    """Edit an existing task for a user."""
    if user not in users:
        print(f"No tasks found for {user}.")
        return

    for task in users[user]:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_priority:
                task['priority'] = new_priority
            if new_due_date:
                task['due_date'] = new_due_date
            if new_category:
                task['category'] = new_category
            print(f"Task ID {task_id} for {user} has been updated.")
            return
    print(f"Task ID {task_id} not found for {user}.")

def delete_task(user, task_id):
    """Delete a task from the task list for a user."""
    if user not in users:
        print(f"No tasks found for {user}.")
        return

    for task in users[user]:
        if task['id'] == task_id:
            confirmation = input(f"Are you sure you want to delete task ID {task_id} for {user}? (yes/no): ")
            if confirmation.lower() == 'yes':
                users[user] = [task for task in users[user] if task['id'] != task_id]
                print(f"Task ID {task_id} for {user} has been deleted.")
                return
            else:
                print("Task deletion canceled.")
                return
    print(f"Task ID {task_id} not found for {user}.")

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

def export_tasks_to_csv(user, filename):
    """Export tasks for a user to a CSV file."""
    if user not in users or not users[user]:
        print(f"No tasks found for {user}.")
        return

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'description', 'priority', 'due_date', 'category', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for task in users[user]:
            writer.writerow(task)

    print(f"Tasks for {user} exported to {filename}.")

def import_tasks_from_csv(user, filename):
    """Import tasks for a user from a CSV file."""
    if user not in users:
        users[user] = []

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = {
                'id': len(users[user]) + 1,
                'description': row['description'],
                'priority': row['priority'],
                'due_date': row['due_date'],
                'category': row['category'],
                'status': row['status']
            }
            users[user].append(task)

    print(f"Tasks for {user} imported from {filename}.")

def main():
    load_tasks_from_file()  # Load tasks from file on startup

    parser = argparse.ArgumentParser(description="Python To-Do List Tracker")
    parser.add_argument('command', choices=['add', 'list', 'complete', 'edit', 'delete', 'export', 'import'], help='Command to execute')
    parser.add_argument('--user', required=True, help='Username for task management')
    parser.add_argument('--description', help='Task description for add or edit command')
    parser.add_argument('--priority', choices=['low', 'medium', 'high'], default=None, help='Task priority for add or edit command')
    parser.add_argument('--due_date', help='Due date for the task (optional)')
    parser.add_argument('--category', help='Task category for add or edit command')
    parser.add_argument('--task_id', type=int, help='Task ID for edit, complete, or delete command')
    parser.add_argument('--filter_by', choices=['priority', 'category'], help='Filter tasks by priority or category')
    parser.add_argument('--filter_value', help='Value for filtering tasks (e.g., "high" for priority, "Work" for category)')
    parser.add_argument('--reminders', action='store_true', help='Show due date reminders')
    parser.add_argument('--sort_by', choices=['description', 'priority', 'due_date', 'status'], help='Sort tasks by a specific field')
    parser.add_argument('--filename', help='Filename for export or import')

    args = parser.parse_args()

    if args.command == 'add':
        if args.description:
            add_task(args.user, args.description, args.priority, args.due_date, args.category)
        else:
            print("Error: Missing task description. Use '--description <task_description>'.")
    elif args.command == 'list':
        list_tasks(args.user, args.filter_by, args.filter_value, args.reminders, args.sort_by)
    elif args.command == 'complete':
        if args.task_id:
            mark_task_complete(args.user, args.task_id)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'edit':
        if args.task_id:
            edit_task(args.user, args.task_id, args.description, args.priority, args.due_date, args.category)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'delete':
        if args.task_id:
            delete_task(args.user, args.task_id)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'export':
        if args.filename:
            export_tasks_to_csv(args.user, args.filename)
        else:
            print("Error: Missing filename. Use '--filename <filename>'.")
    elif args.command == 'import':
        if args.filename:
            import_tasks_from_csv(args.user, args.filename)
        else:
            print("Error: Missing filename. Use '--filename <filename>'.")

    save_tasks_to_file()  # Save tasks to file after each modification

if __name__ == "__main__":
    main()
