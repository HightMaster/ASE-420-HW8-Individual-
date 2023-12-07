import sqlite3
import sys
from datetime import datetime
from datetime import time
import os

print(os.getcwd() + '\\tasks.db')

# Function to create a tasks table
def create_tasks_table():
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            StartTime TEXT NOT NULL,
            EndTime TEXT NOT NULL,
            Tag TEXT,
            TaskDescription TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

# Function to insert a new task
def create_task(date, start_time, end_time, tag, task_description):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    cursor = connection.cursor()
    date = convert_date_string_to_standard(date)

    cursor.execute('''
        INSERT INTO tasks (Date, StartTime, EndTime, Tag, TaskDescription)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, start_time, end_time, tag, task_description))

    connection.commit()
    connection.close()
    print("New task created")

# Function to read all tasks
def read_tasks():
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    connection.close()
    return tasks

# Function to query tasks by individual attributes
def query_tasks(attribute, value):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    cursor = connection.cursor()
    attributes = ["Date", "StartTime", "EndTime", "Tag", "TaskDescription"]
    # Use the LIKE operator to check if the attribute contains the value
    cursor.execute(f'SELECT * FROM tasks WHERE {attribute} LIKE ?', ('%' + value + '%',))
    tasks = cursor.fetchall()

    connection.close()
    return tasks

def query_tasks_by_date(value):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    print("Retrieving all tasks with date: " + value)
    cursor = connection.cursor()
    # Use the LIKE operator to check if the attribute contains the value
    cursor.execute(f'SELECT * FROM tasks WHERE Date LIKE ?', ('%' + value + '%',))
    tasks = cursor.fetchall()

    connection.close()
    return tasks

def query_tasks_by_tag(value):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    print("Retrieving all tasks with tag: " + value)
    cursor = connection.cursor()
    # Use the LIKE operator to check if the attribute contains the value
    cursor.execute(f'SELECT * FROM tasks WHERE Tag LIKE ?', ('%' + value + '%',))
    tasks = cursor.fetchall()

    connection.close()
    return tasks

def query_tasks_by_description(value):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    print("Retrieving all tasks with description: " + value)
    cursor = connection.cursor()
    # Use the LIKE operator to check if the attribute contains the value
    cursor.execute('SELECT * FROM tasks WHERE TaskDescription LIKE ?', ('%' + value + '%',))
    tasks = cursor.fetchall()

    connection.close()
    return tasks
# Function to update a task
# def update_task(task_id, new_date, new_start_time, new_end_time, new_tag, new_task_description):
#     connection = sqlite3.connect(os.getcwd() + 'tasks.db')
#     cursor = connection.cursor()
#
#     cursor.execute('''
#         UPDATE tasks
#         SET Date = ?, StartTime = ?, EndTime = ?, Tag = ?, TaskDescription = ?
#         WHERE id = ?
#     ''', (new_date, new_start_time, new_end_time, new_tag, new_task_description, task_id))
#
#     connection.commit()
#     connection.close()

# Function to delete a task
def delete_task(task_id):
    connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    connection.commit()
    connection.close()

def delete_all_tasks():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(os.getcwd() + '\\tasks.db')
        cursor = connection.cursor()

        # Execute a SQL query to delete all records from your table
        cursor.execute('DELETE FROM tasks')

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        print("All tasks deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def convert_to_time(time_string, possible_formats=None):
    if possible_formats is None:
        # Default formats to try
        possible_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']

    for time_format in possible_formats:
        try:
            time_object = time.strptime(time_string, time_format)
            return time_object
        except ValueError:
            pass

    print(f"Error: Unable to convert {time_string} to time using any of the specified formats.")
    return None

#Converts string date into proper string date format
def convert_date_string_to_standard(date_string, possible_formats=None):
    if possible_formats is None:
        # Default formats to try
        #possible_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']
        possible_formats = ['%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y']

    if "today" in date_string:
        return datetime.today().strftime('%Y/%m/%d')

    print("Trying date")
    for date_format in possible_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            return date_object.strftime('%Y/%m/%d')
        except ValueError as e:
            pass

    print(f"Error: Unable to convert {date_string} to datetime using any of the specified formats.")
    return None

#converts string date into date object
def convert_string_date_to_object(date_string, possible_formats=None):
    if possible_formats is None:
        # Default formats to try
        #possible_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']
        possible_formats = ['%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y']

    if "today" in date_string:
        return datetime.today()

    for date_format in possible_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            return date_object
        except ValueError as e:
            pass

    print(f"Error: Unable to convert {date_string} to datetime using any of the specified formats.")
    return None

def format_tasks(tasks):
    if len(tasks) == 0:
        return "No tasks"

    formatted_tasks = []
    for task in tasks:
        formatted_task = f"""-----------------------\nTask ID: {task[0]}\nDate: {task[1]}\nStart Time: {task[2]}\nEnd Time: {task[3]}\nTag: {task[4]}\nTask Description: {task[5]}\n"""
        formatted_tasks.append(formatted_task)

    return '\n'.join(formatted_tasks)

# Example usage
if __name__ == "__main__":
    # Create tasks table
    #create_tasks_table()
    #print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\src")
    print(sys.path)
    # Create tasks
    # create_task('2023-01-01', '08:00', '10:00', 'Work', 'Complete project report')
    # create_task('2023-01-02', '12:00', '14:00', 'Personal', 'Exercise and jogging')

    # Update a task
    # update_task(1, '2023-01-01', '08:30', '10:30', 'Work', 'Complete project report and submit')

