import sqlite3
import sys
import os
from datetime import datetime
from datetime import time
from datetime import datetime

class TimeHelper:
    _instance = None  # Class variable to store the instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeHelper, cls).__new__(cls)
        return cls._instance

    # Private constructor to prevent multiple instances
    def __init__(self):
        pass

    @staticmethod
    def convert_time_string_to_standard(time_string, possible_formats=None):
        if possible_formats is None:
            possible_formats = ['%H:%M', '%I:%M%p', '%H:%M%p', '%I:%M %p']

        for time_format in possible_formats:
            try:
                time_object = datetime.strptime(time_string, time_format)
                return time_object.strftime('%I:%M%p')
            except ValueError:
                pass

        print(f"Error: Unable to convert {time_string} to time using any of the specified formats.")
        return None

    @staticmethod
    def convert_string_time_to_object(time_string, possible_formats=None):
        if possible_formats is None:
            possible_formats = ['%H:%M', '%I:%M%p', '%H:%M%p', '%I:%M %p', '%I:%M']

        for time_format in possible_formats:
            try:
                time_object = datetime.strptime(time_string, time_format)
                return time_object
            except ValueError:
                pass

        print(f"Error: Unable to convert {time_string} to time using any of the specified formats.")
        return None
