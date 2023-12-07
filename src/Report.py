from Command import Command
# Function to parse the input string into individual components
from src import db_crud
import re
from datetime import datetime
from DateHelper import DateHelper
from TimeHelper import TimeHelper

class Report(Command):
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def get_command(self):
        return self.command
    def execute(self):
        return db_crud.format_tasks(db_crud.query_longest_tasks())
