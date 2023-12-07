from Command import Command
from src import db_crud
from Report import Report
class ReportBuilder:
    def __init__(self):
        self.report = Report()

    def add_command(self, command):
        self.report.set_command(command)

    def build(self):
        return self.report