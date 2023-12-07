import pytest
import sys, os
import sys
import os
from datetime import datetime
import sqlite3
from src.DateHelper import DateHelper
from src.TimeHelper import TimeHelper
from src.Report import Report
from src.ReportBuilder import ReportBuilder
from src.db_crud import (
    create_tasks_table,
    create_task,
    read_tasks,
    query_tasks_by_description,
    delete_task,
    delete_all_tasks,
    format_tasks,
    query_longest_tasks
)

"""
NOTE: Integration test file contains all tests related to new features and ensuring they can still integrate
with old features in the code base. Not All database functionalities need to be tested here, just the ones for 
integration. 
"""

dbpath = os.path.join(os.getcwd(), 'tasks.db') # directory path of the app
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

def test_query_longest_tasks(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    create_task('2023/01/01', '07:00', '10:00', 'Work', 'School')
    tasks = query_longest_tasks()
    assert "School" in tasks[1]

# Test the create_task function
def test_create_task(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    tasks = []
    tasks.append(read_tasks())
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
    standard_date = DateHelper.convert_date_string_to_standard('2023-01-01')
    assert standard_date == '2023/01/01'

# Test the convert_string_date_to_object function
def test_convert_string_date_to_object():
    date_object = DateHelper.convert_string_date_to_object('2023/01/01')
    assert date_object.strftime('%Y/%m/%d')

def test_convert_time_string_to_standard():
    time1 = TimeHelper.convert_time_string_to_standard("09:00AM")
    time2 = TimeHelper.convert_time_string_to_standard("09:00")
    time3 = TimeHelper.convert_time_string_to_standard("9:00")
    assert time1 == time2
    assert time3 == time1
    assert time3 == time2

def test_string_time_to_object():
    time1 = TimeHelper.convert_time_string_to_standard("09:00AM")
    time2 = TimeHelper.convert_time_string_to_standard("09:00")
    time3 = TimeHelper.convert_time_string_to_standard("9:00")
    assert time1 == time2
    assert time3 == time1
    assert time3 == time2

def test_report_builder(setup_teardown_database):
    report_builder = ReportBuilder()
    report_builder.add_command("Report")
    create_task('2023/01/01', '08:00', '10:00', ':WORK', 'Complete project report')
    create_task('2023/01/01', '08:00', '10:00', ':SCHOOL', 'Complete project report')
    report_command = report_builder.build()
    assert report_command.get_command() == "Report"

def test_report_execute(setup_teardown_database):
    report_builder = ReportBuilder()
    report_builder.add_command("Report")
    create_task('2023/01/01', '08:00', '10:00', ':WORK', 'Complete project report')
    create_task('2023/01/01', '08:00', '10:00', ':SCHOOL', 'Complete project report')
    report_command = report_builder.build()
    print(report_command.execute())
    assert ":WORK" in report_command.execute()
    assert ":SCHOOL" in report_command.execute()

# Test the format_tasks function
def test_format_tasks():
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    formatted_task = format_tasks(query_tasks_by_description("Complete"))
    assert isinstance(formatted_task, str)