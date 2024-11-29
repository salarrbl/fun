import os
import subprocess
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama for text coloring
init(autoreset=True)

# Directory for daily task files
TODO_DIR = "tasks"
os.makedirs(TODO_DIR, exist_ok=True)

def get_date():
    """Get today's date as a string."""
    return datetime.now().strftime("%Y-%m-%d")

def get_todo_file(date=None):
    """Get a todo file path for a given date (or today)."""
    if not date:
        date = get_date()
    return os.path.join(TODO_DIR, f"{date}_todo.txt")

def get_done_file(date=None):
    """Get a done file path for a given date (or today)."""
    if not date:
        date = get_date()
    return os.path.join(TODO_DIR, f"{date}_done.txt")

def load_tasks(file):
    """Load tasks from a file."""
    if os.path.exists(file):
        with open(file, 'r') as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_tasks(file, tasks):
    """Save tasks to a file."""
    with open(file, 'w') as f:
        f.writelines(task + '\n' for task in tasks)

def list_tasks():
    """Display all active tasks."""
    tasks = load_tasks(get_todo_file())
    if tasks:
        print(Fore.CYAN + "\nToday's Tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{Fore.YELLOW}{i}. {Style.BRIGHT}{task}")
    else:
        print(Fore.YELLOW + "No tasks found for today. Add some tasks to get started!")

def add_task():
    """Add a new task."""
    task = input("Enter the task: ").strip()
    if task:
        tasks = load_tasks(get_todo_file())
        tasks.append(task)
        save_tasks(get_todo_file(), tasks)
        print(Fore.GREEN + f"Task added: {task}")
    else:
        print(Fore.RED + "Task cannot be empty!")

def mark_task_done():
    """Mark a task as done."""
    todo_file = get_todo_file()
    done_file = get_done_file()

    tasks = load_tasks(todo_file)
    if not tasks:
        print(Fore.YELLOW + "No tasks to mark as done!")
        return

    list_tasks()
    try:
        task_num = int(input("\nEnter the task number to mark as done: "))
        if 1 <= task_num <= len(tasks):
            task = tasks.pop(task_num - 1)
            save_tasks(todo_file, tasks)

            # Add to done file
            completed_tasks = load_tasks(done_file)
            completed_tasks.append(task)
            save_tasks(done_file, completed_tasks)

            print(Fore.GREEN + f"Marked task as done: {task}")
        else:
            print(Fore.RED + "Invalid task number. Please try again.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid number.")

def view_done_tasks():
    """View all completed tasks for today."""
    done_tasks = load_tasks(get_done_file())
    if done_tasks:
        print(Fore.CYAN + "\nToday's Completed Tasks:")
        for i, task in enumerate(done_tasks, start=1):
            print(f"{Fore.GREEN}{i}. {Style.BRIGHT}{task}")
    else:
        print(Fore.YELLOW + "No completed tasks for today.")

def generate_monthly_chart():
    result = subprocess.run(['python', 'chart.py'], capture_output=True, text=True)
    output = result.stdout
    print(output)

def main_menu():
    """Main menu for task management."""
    while True:
        print(Fore.CYAN + """\nOptions:"
        1. List today's tasks
        2. Add a task
        3. Mark a task as done
        4. View completed tasks
        5. Generate monthly chart
        6. Exit""" + Fore.RESET)

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == '1':
            list_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            mark_task_done()
        elif choice == '4':
            view_done_tasks()
        elif choice == '5':
            generate_monthly_chart()
        elif choice == '6':
            print(Fore.CYAN + "Goodbye! Stay productive!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    print(Fore.MAGENTA + Style.BRIGHT + "Welcome to the Daily Todo Manager with Monthly Chart!")
    main_menu()

