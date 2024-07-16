import argparse

# Sample initial task list (will be replaced with persistence in later iterations)
tasks = []

def add_task(task_description):
    """Add a new task to the task list."""
    tasks.append(task_description)
    print(f"Task added: '{task_description}'")

def list_tasks():
    """Display all tasks in the task list."""
    if tasks:
        print("Tasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")
    else:
        print("No tasks found.")

def main():
    parser = argparse.ArgumentParser(description="Python To-Do List Tracker")
    parser.add_argument('command', choices=['add', 'list'], help='Command to execute')
    parser.add_argument('task_description', nargs='?', default='', help='Task description for add command')

    args = parser.parse_args()

    if args.command == 'add':
        if args.task_description:
            add_task(args.task_description)
        else:
            print("Error: Missing task description. Use 'add <task_description>'.")
    elif args.command == 'list':
        list_tasks()

if __name__ == "__main__":
    main()
