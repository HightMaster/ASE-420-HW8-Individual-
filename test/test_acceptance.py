import pytest
import sys, os
import sys
import os
from datetime import datetime
import sqlite3
from src.DateHelper import DateHelper
from src.TimeHelper import TimeHelper
from src.ReportBuilder import ReportBuilder
from src.Report import Report
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
NOTE: Acceptance test file contains all tests related to new features and old features in combination.
This is as opposed to regression tests which pretty much run all Unit tests for old features to make sure
they still work properly on their own. 
"""

create_tasks_table()
dbpath = os.path.join(os.getcwd(), 'tasks.db')  # directory path of the app

@pytest.fixture
def setup_teardown_database():
    connection = sqlite3.connect(dbpath)
    create_tasks_table()
    delete_all_tasks()

def test_query_longest_tasks(setup_teardown_database):
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')
    create_task('2023/01/01', '07:00', '10:00', 'Work', 'School')
    tasks = query_longest_tasks()
    assert "School" in tasks[1]

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

def test_convert_string_date_to_object():
    date_object = DateHelper.convert_string_date_to_object("05-08-2002")
    assert date_object == datetime(2002, 5, 8, 0, 0, 0)

def test_convert_date_string_to_standard():
    assert DateHelper.convert_date_string_to_standard("05-08-2002") == DateHelper.convert_date_string_to_standard("2002-05-08")

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