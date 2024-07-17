import argparse
import json
from datetime import datetime, timedelta

# Initialize tasks list (will store dictionary objects for enhanced details)
tasks = []

def add_task(task_description, priority='low', due_date=None, category=None):
    """Add a new task to the task list."""
    task = {
        'id': len(tasks) + 1,
        'description': task_description,
        'priority': priority,
        'due_date': due_date,
        'category': category,
        'status': 'pending'  # Default status
    }
    tasks.append(task)
    print(f"Task added: '{task_description}'")

def list_tasks(category_filter=None):
    """Display all tasks in the task list, optionally filtered by category."""
    if tasks:
        print("Tasks:")
        for task in tasks:
            if category_filter and task['category'] != category_filter:
                continue
            print(f"ID: {task['id']}, Description: {task['description']}, Priority: {task['priority']}, Due Date: {task['due_date']}, Category: {task['category']}, Status: {task['status']}")
    else:
        print("No tasks found.")

def list_upcoming_tasks(days=3):
    """Display tasks with due dates approaching within the specified number of days."""
    upcoming_tasks = []
    now = datetime.now()
    for task in tasks:
        if task['due_date']:
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
            if now <= due_date <= now + timedelta(days=days):
                upcoming_tasks.append(task)
    if upcoming_tasks:
        print(f"Tasks due within {days} days:")
        for task in upcoming_tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Due Date: {task['due_date']}, Priority: {task['priority']}, Category: {task['category']}, Status: {task['status']}")
    else:
        print(f"No tasks due within the next {days} days.")

def mark_task_complete(task_id):
    """Mark a task as complete."""
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            print(f"Task ID {task_id} marked as completed.")
            return
    print(f"Error: Task ID {task_id} not found.")

def edit_task(task_id, new_description=None, new_priority=None, new_due_date=None, new_category=None):
    """Edit an existing task."""
    for task in tasks:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_priority:
                task['priority'] = new_priority
            if new_due_date:
                task['due_date'] = new_due_date
            if new_category:
                task['category'] = new_category
            print(f"Task ID {task_id} has been updated.")
            return
    print(f"Error: Task ID {task_id} not found.")

def delete_task(task_id):
    """Delete a task from the task list."""
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            confirmation = input(f"Are you sure you want to delete task ID {task_id}? (yes/no): ")
            if confirmation.lower() == 'yes':
                tasks = [task for task in tasks if task['id'] != task_id]
                print(f"Task ID {task_id} has been deleted.")
                return
            else:
                print("Task deletion canceled.")
                return
    print(f"Error: Task ID {task_id} not found.")

def save_tasks_to_file(filename='tasks.json'):
    """Save tasks to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

def load_tasks_from_file(filename='tasks.json'):
    """Load tasks from a JSON file."""
    global tasks
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []  # Start with an empty list if file doesn't exist

def main():
    load_tasks_from_file()  # Load tasks from file on startup

    parser = argparse.ArgumentParser(description="Python To-Do List Tracker")
    parser.add_argument('command', choices=['add', 'list', 'complete', 'edit', 'delete', 'upcoming'], help='Command to execute')
    parser.add_argument('--description', help='Task description for add or edit command')
    parser.add_argument('--priority', choices=['low', 'medium', 'high'], default=None, help='Task priority for add or edit command')
    parser.add_argument('--due_date', help='Due date for the task (optional)')
    parser.add_argument('--category', help='Task category for add or edit command')
    parser.add_argument('--task_id', type=int, help='Task ID for edit, complete, or delete command')
    parser.add_argument('--days', type=int, default=3, help='Number of days for upcoming tasks filter')

    args = parser.parse_args()

    if args.command == 'add':
        if args.description:
            add_task(args.description, args.priority, args.due_date, args.category)
        else:
            print("Error: Missing task description. Use '--description <task_description>'.")
    elif args.command == 'list':
        list_tasks(args.category)
    elif args.command == 'complete':
        if args.task_id:
            mark_task_complete(args.task_id)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'edit':
        if args.task_id:
            edit_task(args.task_id, args.description, args.priority, args.due_date, args.category)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'delete':
        if args.task_id:
            delete_task(args.task_id)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")
    elif args.command == 'upcoming':
        list_upcoming_tasks(args.days)

    save_tasks_to_file()  # Save tasks to file after each modification

if __name__ == "__main__":
    main()
