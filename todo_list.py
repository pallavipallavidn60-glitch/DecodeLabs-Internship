import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    """
    Loads tasks from disk to beat the 'Volatile Trap' (Page 13-14).
    If the file doesn't exist, it returns an empty list (The Zero of Lists).
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_tasks(tasks):
    """
    Saves the list of dictionaries to disk using Serialization (JSON).
    This moves data from RAM (Volatile) to DISK (Permanent).
    """
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, task_name):
    """
    Implements the 'In-Memory Database' concept (Page 16).
    Creates a dictionary (like a SQL row) and appends it to the list.
    """
    # Generate a new ID (like a Primary Key)
    task_id = len(tasks) + 1
    
    # Create the dictionary structure (Dictionary -> Table Row)
    new_task = {
        "id": task_id,
        "task": task_name,
        "completed": False
    }
    
    # Append is O(1) amortized - the core skill from Page 8
    tasks.append(new_task)
    
    # Save to disk so data persists
    save_tasks(tasks)
    print(f"\n✅ Task added successfully: '{task_name}' (ID: {task_id})")

def view_tasks(tasks):
    """
    Implements the 'Display: The Read Operation' (Page 10).
    Uses enumerate() for Professional Polish (Page 11).
    """
    if not tasks:
        print("\n📭 Your to-do list is empty. Add a task first!")
        return

    print("\n" + "="*40)
    print("       📋 YOUR TO-DO LIST")
    print("="*40)
    
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task.get("completed") else "⬜"
        print(f"  {index}. {status} [ID: {task['id']}] {task['task']}")
    
    print("="*40)

def mark_completed(tasks):
    """Bonus Feature: Mark a task as completed (Process/Modify data)."""
    if not tasks:
        print("\n📭 No tasks to mark.")
        return
    
    view_tasks(tasks)
    try:
        task_num = int(input("\nEnter the task number to mark as completed: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["completed"] = True
            save_tasks(tasks)
            print(f"✅ Task '{tasks[task_num - 1]['task']}' marked as completed!")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def delete_task(tasks):
    """Bonus Feature: Delete a task (Process/Modify data)."""
    if not tasks:
        print("\n📭 No tasks to delete.")
        return
    
    view_tasks(tasks)
    try:
        task_num = int(input("\nEnter the task number to delete: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            # Re-assign IDs to keep them sequential
            for i, task in enumerate(tasks, start=1):
                task["id"] = i
            save_tasks(tasks)
            print(f"🗑️ Task '{removed['task']}' deleted successfully!")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def display_menu():
    """Displays the main menu options."""
    print("\n" + "-"*40)
    print("   MAIN MENU")
    print("-"*40)
    print("  1. ➕ Add a Task       (Input)")
    print("  2. 📋 View Tasks       (Output)")
    print("  3. ✅ Mark as Done     (Process)")
    print("  4. 🗑️ Delete a Task    (Process)")
    print("  5. 🚪 Exit")
    print("-"*40)

def main():
    """
    The main entry point of the application (Page 19).
    Implements the IPO Model: Input -> Process -> Output (Page 6).
    """
    # Initialize the memory container (Page 7)
    my_tasks = load_tasks()
    
    print("\n" + "="*40)
    print("  DecodeLabs Project 1: The To-Do List")
    print("  Junior Python Developer - Logic Phase")
    print("="*40)
    print(f"  📂 Loaded {len(my_tasks)} task(s) from disk.")

    while True:
        display_menu()
        choice = input("  Enter your choice (1-5): ").strip()

        # --- INPUT PHASE ---
        if choice == "1":
            task_input = input("\n  Enter the task description: ").strip()
            if task_input:
                add_task(my_tasks, task_input)
            else:
                print("  ⚠️ Task cannot be empty. Please try again.")
        
        # --- OUTPUT PHASE ---
        elif choice == "2":
            view_tasks(my_tasks)
        
        # --- PROCESS PHASE ---
        elif choice == "3":
            mark_completed(my_tasks)
        
        # --- PROCESS PHASE ---
        elif choice == "4":
            delete_task(my_tasks)
        
        # --- EXIT ---
        elif choice == "5":
            print("\n" + "="*40)
            print("  👋 Goodbye! Your tasks are safely saved.")
            print("  Remember: RAM is volatile, but JSON persists!")
            print("="*40)
            break
        
        else:
            print("\n  ⚠️ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()