import sqlite3
import sys
from datetime import datetime
from datetime import time
import os
from DateHelper import DateHelper
from TimeHelper import TimeHelper

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
    date = DateHelper.convert_date_string_to_standard(date)

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

def query_tasks_by_date_range(startDate, endDate):
    startDate = DateHelper.convert_date_string_to_standard(startDate)
    endDate = DateHelper.convert_date_string_to_standard(endDate)
    tasks = read_tasks()
    new_task_list = []
    date_index = 1
    for task in tasks:
        taskDate = DateHelper.convert_string_date_to_object(task[date_index])
        if taskDate >= DateHelper.convert_string_date_to_object(startDate) and taskDate <= DateHelper.convert_string_date_to_object(endDate):
            new_task_list.append(task)
    return new_task_list

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

#Function to query longest tasks in sorted list
def query_longest_tasks():
    tasks = read_tasks()
    new_task_list = []
    for task in tasks:
        #Defining indexes
        start_time_index = 2
        end_time_index = 3
        #Defining time variables for calculations
        previous_start_time = datetime(2023, 1, 1, 0, 0, 0)
        previous_end_time = datetime(2023, 1, 1, 0, 0, 0)
        start_time = TimeHelper.convert_string_time_to_object(task[start_time_index])
        end_time = TimeHelper.convert_string_time_to_object(task[end_time_index])
        #If time for task is longer than put it at the beginning of the report
        if abs(start_time - end_time) > abs(previous_start_time - previous_end_time):
            # new_task_list.insert(0, task)
            new_task_list.append(task)
            previous_start_time = start_time
            previous_end_time = end_time
    return new_task_list

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

def format_tasks(tasks):
    if len(tasks) == 0:
        return "No tasks"

    formatted_tasks = []
    for task in tasks:
        one_hour = datetime(2023, 1, 1, 1, 0, 0) - datetime(2023, 1, 1, 0, 0, 0)
        taskTime = abs(TimeHelper.convert_string_time_to_object(task[2]) - TimeHelper.convert_string_time_to_object(task[3]))
        if taskTime < one_hour:
            taskTime = str(taskTime) + "mins"
        else:
            taskTime = str(taskTime) + "hrs"
        formatted_task = f"""-----------------------\nTask ID: {task[0]}\nDate: {task[1]}\nStart Time: {task[2]}\nEnd Time: {task[3]}\nLength: {taskTime}\nTag: {task[4]}\nTask Description: {task[5]}"""
        formatted_tasks.append(formatted_task)

    return '\n'.join(formatted_tasks)

# Example usage
if __name__ == "__main__":
    # Create tasks table
    #create_tasks_table()
    #print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\src")
    print(format_tasks(query_longest_tasks()))
    # Create tasks
    # create_task('2023-01-01', '08:00', '10:00', 'Work', 'Complete project report')
    # create_task('2023-01-02', '12:00', '14:00', 'Personal', 'Exercise and jogging')

    # Update a task
    # update_task(1, '2023-01-01', '08:30', '10:30', 'Work', 'Complete project report and submit')

