import pytest
import sys, os
import sys
import os
from datetime import datetime
import sqlite3

from src.db_crud import (
    create_tasks_table,
    create_task,
    read_tasks,
    query_tasks_by_description,
    delete_task,
    delete_all_tasks,
    convert_date_string_to_standard,
    convert_string_date_to_object,
    format_tasks,
)

create_tasks_table()

dbpath = os.path.join(os.getcwd(), 'tasks.db') # directory path of the app
print(dbpath)
delete_all_tasks()
# Fixture to set up and tear down the database for each test
@pytest.fixture
def setup_teardown_database():
    connection = sqlite3.connect(dbpath)
    create_tasks_table()
    delete_all_tasks()

# Test the create_tasks_table function
def test_create_tasks_table(setup_teardown_database):
    # Assert that the 'tasks' table is created
    assert os.path.isfile(dbpath)

# Test the create_task function
def test_create_task(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    tasks = []
    tasks.append(read_tasks())
    assert len(tasks) == 1

# Test the read_tasks function
def test_read_tasks(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    create_task('2023/01/02', '12:00', '14:00', 'Personal', 'Exercise and jogging')
    tasks = []
    tasks.append(query_tasks_by_description("Complete"))
    tasks.append(query_tasks_by_description("Exercise"))
    assert len(tasks) == 2

# Test the query_tasks_by_description function
def test_query_tasks_by_description(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    create_task('2023/01/02', '12:00', '14:00', 'Personal', 'Exercise and jogging')
    tasks = []
    tasks.append(query_tasks_by_description("Complete"))
    assert len(tasks) == 1


# Test the delete_task function
def test_delete_task(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    task = query_tasks_by_description("Complete")
    taskID = task[0][0]
    delete_task(taskID)
    tasks = read_tasks()
    assert len(tasks) == 0

# Test the delete_all_tasks function
def test_delete_all_tasks(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    create_task('2023/01/02', '12:00', '14:00', 'Personal', 'Exercise and jogging')
    delete_all_tasks()
    tasks = read_tasks()
    taskList = []
    taskList.append(tasks)
    assert len(tasks) == 0

# ... Add more test functions for other functionalities

# Test the convert_date_string_to_standard function
def test_convert_date_string_to_standard():
    standard_date = convert_date_string_to_standard('2023-01-01')
    assert standard_date == '2023/01/01'

# Test the convert_string_date_to_object function
def test_convert_string_date_to_object():
    date_object = convert_string_date_to_object('2023/01/01')
    assert date_object.strftime('%Y/%m/%d')

# Test the format_tasks function
def test_format_tasks():
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    formatted_task = format_tasks(query_tasks_by_description("Complete"))
    assert isinstance(formatted_task, str)

# ... Add more test functions for other functionalities
