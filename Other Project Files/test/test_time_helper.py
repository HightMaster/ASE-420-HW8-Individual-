from datetime import datetime
from src.TimeHelper import TimeHelper  # Replace 'your_module' with the actual module name

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
