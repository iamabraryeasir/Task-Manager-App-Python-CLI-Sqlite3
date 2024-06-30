# Imposing necessary modules
import sqlite3
from os import name, system
from prettytable import PrettyTable

##################   Doing all DB Setup   ##################
con = sqlite3.connect('task_manager.db')

cursor = con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                deadline TEXT NOT NULL                  
            )
''')

##################    Custom Table Setup   ##################

# Creating table Object to Beautifully print the Output
table = PrettyTable(['Index', 'Task', 'Deadline'])

# Formatting the table alignment. 
table.align['Index'] = "c"
table.align['Task'] = "l"
table.align['Deadline'] = "r"


def list_tasks():
    clear_screen()
    table.clear_rows()
    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        table.add_row([row[0], row[1], row[2]])
    
    print(table)

def add_task(task, deadline):
    cursor.execute("INSERT INTO tasks (task, deadline) VALUES (?, ?)", (task, deadline))
    con.commit()


def update_task(task_id, new_task, new_deadline):
    cursor.execute("UPDATE tasks SET task = ? , deadline = ? WHERE id = ?", (new_task, new_deadline, task_id))
    con.commit()
    



def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()
    renumber_ids()

def renumber_ids():
    cursor.execute("SELECT id FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    for index, (task_id,) in enumerate(rows, start=1):
        cursor.execute("UPDATE tasks SET id = ? WHERE id = ?", (index, task_id))
    con.commit()


def clear_screen():         # To clear the screen before running the new code.
    if name == 'nt':        # for windows
        _ = system('cls')

    else:                   # for mac and linux(here, os.name is 'posix')
        _ = system('clear')


def main():
    clear_screen()
    
    # Printing the app title.
    print("             **********************************")
    print("             *       Task Manager CLI App     *")
    print("             **********************************")

    while True:
        # Printing the options for user choice.
        print("\n1. List All Stored Tasks")
        print("2. Add a New Task")
        print("3. Update Some Details")
        print("4. Delete a Task")
        print("5. Exit the App\n")  

        # Taking user input with proper validation.
        while True:
            user_choice = int(input("What do you want to do: "))
            if user_choice in [1, 2, 3, 4, 5]:
                break
            print("Invalid Choice.!!!")
        
                # Triggering methods based on user choice
        match user_choice:
            case 1:
                list_tasks()
            
            case 2:
                task = input("Enter the task name: ")
                deadline = input("Enter the task deadline: ")
                add_task(task, deadline)
                list_tasks()
            
            case 3:
                while True:
                    task_id = int(input("Enter the task id to update: "))
                    cursor.execute("SELECT * FROM tasks")
                    if 1 <= task_id <= len(cursor.fetchall()):
                        break
                task = input("Enter new task name: ")
                deadline = input("Enter new task deadline: ")
                update_task(task_id, task, deadline)
                list_tasks()

            case 4:
                task_id = input("Enter the task id to delete: ")
                delete_task(task_id)
                list_tasks()
            
            case 5:
                break
    
    con.close() # closing database connection.

if __name__ == "__main__":
    main()