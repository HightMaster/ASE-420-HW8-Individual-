import sqlite3
import sys
from datetime import time
import os
from datetime import datetime

class DateHelper:
    _instance = None  # Class variable to store the instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DateHelper, cls).__new__(cls)
        return cls._instance

    # Private constructor to prevent multiple instances
    def __init__(self):
        pass

    @staticmethod
    def convert_date_string_to_standard(date_string, possible_formats=None):
        if possible_formats is None:
            possible_formats = ['%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y',
                                '%m-%d-%y']

        if "today" in date_string:
            return datetime.today().strftime('%Y/%m/%d')

        for date_format in possible_formats:
            try:
                date_object = datetime.strptime(date_string, date_format)
                return date_object.strftime('%Y/%m/%d')
            except ValueError as e:
                pass

        print(f"Error: Unable to convert {date_string} to datetime using any of the specified formats.")
        return None

    @staticmethod
    def convert_string_date_to_object(date_string, possible_formats=None):
        if possible_formats is None:
            possible_formats = ['%Y/%m/%d', '%y/%m/%d', '%Y-%m-%d', '%y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y',
                                '%m-%d-%y']

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

