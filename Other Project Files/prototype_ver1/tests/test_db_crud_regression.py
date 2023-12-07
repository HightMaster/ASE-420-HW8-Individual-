import pytest
import os
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

# Fixture to set up and tear down the database for each test
@pytest.fixture
def setup_teardown_database():
    create_tasks_table()
    yield
    delete_all_tasks()

# Test the create_tasks_table function
def test_create_tasks_table(setup_teardown_database):
    # Assert that the 'tasks' table exists
    assert os.path.isfile('tasks.db')

# Regression test for read_tasks
def test_read_tasks_regression(setup_teardown_database):
    # Create a sample task
    create_task('2023/01/01', '08:00', '10:00', 'Work', 'Complete project report')

    # Read tasks and check if the task is present in the result
    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0][5] == 'Complete project report'

# Test the convert_date_string_to_standard function
def test_convert_date_string_to_standard():
    # Test with a valid date string
    result = convert_date_string_to_standard('2023-01-01')
    assert result == '2023/01/01'

    # Test with another valid date string
    result = convert_date_string_to_standard('01/15/2023')
    assert result == '2023/01/15'

    # Test with an invalid date string
    result = convert_date_string_to_standard('invalid_date')
    assert result is None

# Test the convert_string_date_to_object function
def test_convert_string_date_to_object():
    # Test with a valid date string
    result = convert_string_date_to_object('2023-01-01')
    assert result is not None

    # Test with another valid date string
    result = convert_string_date_to_object('01/15/2023')
    assert result is not None

    # Test with an invalid date string
    result = convert_string_date_to_object('invalid_date')
    assert result is None
