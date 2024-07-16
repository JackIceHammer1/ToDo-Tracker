import argparse
import json

# Initialize tasks list (will store dictionary objects for enhanced details)
tasks = []

def add_task(task_description, priority='low', due_date=None):
    """Add a new task to the task list."""
    task = {
        'id': len(tasks) + 1,
        'description': task_description,
        'priority': priority,
        'due_date': due_date,
        'status': 'pending'  # Default status
    }
    tasks.append(task)
    print(f"Task added: '{task_description}'")

def list_tasks():
    """Display all tasks in the task list."""
    if tasks:
        print("Tasks:")
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Priority: {task['priority']}, Status: {task['status']}")
    else:
        print("No tasks found.")

def mark_task_complete(task_id):
    """Mark a task as complete."""
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            print(f"Task ID {task_id} marked as completed.")
            return
    print(f"Task ID {task_id} not found.")

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
    parser.add_argument('command', choices=['add', 'list', 'complete'], help='Command to execute')
    parser.add_argument('--description', help='Task description for add command')
    parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='low', help='Task priority for add command')
    parser.add_argument('--due_date', help='Due date for the task (optional)')
    parser.add_argument('--task_id', type=int, help='Task ID to mark as complete')

    args = parser.parse_args()

    if args.command == 'add':
        if args.description:
            add_task(args.description, args.priority, args.due_date)
        else:
            print("Error: Missing task description. Use '--description <task_description>'.")
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'complete':
        if args.task_id:
            mark_task_complete(args.task_id)
        else:
            print("Error: Missing task ID. Use '--task_id <task_id>'.")

    save_tasks_to_file()  # Save tasks to file after each modification

if __name__ == "__main__":
    main()
