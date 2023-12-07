import pytest
from datetime import datetime
from src.DateHelper import DateHelper  # Replace 'your_module' with the actual module name

def test_convert_string_date_to_object():
    date_object = DateHelper.convert_string_date_to_object("05-08-2002")
    assert date_object == datetime(2002, 5, 8, 0, 0, 0)

def test_convert_date_string_to_standard():
    assert DateHelper.convert_date_string_to_standard("05-08-2002") == DateHelper.convert_date_string_to_standard("2002-05-08")
