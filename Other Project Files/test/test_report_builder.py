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
)

create_tasks_table()

dbpath = os.path.join(os.getcwd(), 'tasks.db')  # directory path of the app
print(dbpath)


@pytest.fixture
def setup_teardown_database():
    connection = sqlite3.connect(dbpath)
    create_tasks_table()
    delete_all_tasks()


def test_report_builder(setup_teardown_database):
    report_builder = ReportBuilder()
    report_builder.add_command("Report")
    create_task('2023/01/01', '08:00', '10:00', ':WORK', 'Complete project report')
    create_task('2023/01/01', '08:00', '10:00', ':SCHOOL', 'Complete project report')
    report_command = report_builder.build()
    assert report_command.get_command() == "Report"
