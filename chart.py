import os
import random
from datetime import datetime, timedelta
from tabulate import tabulate

# Directory for daily task files
TODO_DIR = "tasks"
os.makedirs(TODO_DIR, exist_ok=True)

def generate_monthly_chart():
    """Generate a simple bar chart and tabular data for completed tasks in the current month."""
    today = datetime.now()
    start_of_month = today.replace(day=1)
    days_in_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)).day

    dates = [(start_of_month + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_in_month)]
    completion_counts = []

    for date in dates:
        done_file = os.path.join(TODO_DIR, f"{date}_done.txt")
        if os.path.exists(done_file):
            completion_counts.append(len(open(done_file).readlines()))
        else:
            completion_counts.append(0)

    # Print the data in a tabular format
    print("\nTask Completion Data (Tabular Format):")
    table_data = [[dates[i], completion_counts[i]] for i in range(days_in_month)]
    print(tabulate(table_data, headers=["Date", "Completed Tasks"], tablefmt="grid"))

    # Generate ASCII bar chart
    print("\nTask Completion Chart (ASCII Bars):")
    for i in range(days_in_month):
        bar = "█" * completion_counts[i]  # Use "█" for the bar
        print(f"{dates[i]}: {bar} ({completion_counts[i]}) tasks completed")

def add_task(date, task):
    """Add a new task to the todo list for a specific date."""
    todo_file = os.path.join(TODO_DIR, f"{date}_todo.txt")
    with open(todo_file, 'a') as f:
        f.write(f"{task}\n")
    print(f"Task added to {date}.")

def mark_task_done(date, task):
    """Mark a task as completed and move it to the done list."""
    todo_file = os.path.join(TODO_DIR, f"{date}_todo.txt")
    done_file = os.path.join(TODO_DIR, f"{date}_done.txt")

    # Check if the task exists in the todo file
    with open(todo_file, 'r') as f:
        tasks = f.readlines()

    task_found = False
    for i, line in enumerate(tasks):
        if task in line:
            task_found = True
            tasks.pop(i)  # Remove task from todo list
            break

    if task_found:
        with open(todo_file, 'w') as f:
            f.writelines(tasks)  # Update todo file without the completed task

        with open(done_file, 'a') as f:
            f.write(f"{task}\n")  # Add task to done file
        print(f"Task marked as done: {task}")
    else:
        print(f"Task '{task}' not found in {date} todo list.")

def display_task_summary():
    """Display a summary of task completions for the month."""
    generate_monthly_chart()

if __name__ == "__main__":
    display_task_summary()  # Display task summary (chart and table)
