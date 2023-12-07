# Function to parse the input string into individual components
from src import db_crud
import re
from datetime import datetime
from DateHelper import DateHelper
from TimeHelper import TimeHelper
from Report import Report
from ReportBuilder import ReportBuilder

def parse_input_string(input_string):
    #Command definition
    command = input_string.split()[0].lower()
    addCommands = ["record", "add", "create"]
    deleteCommands = ["delete", "remove"]
    queryCommands = ["query", "search"]
    reportCommands = ["report"]
    command_index = 1
    endTime_index = 1
    #Run if adding new tasks
    if command in addCommands:
        try:
            date = input_string.split()[command_index]
            taskDescription = re.search(r'(\'|\")(.*?)(\'|\")', input_string).group()
            taskDescription = taskDescription.replace("\'", "")
            startTime = re.search(r'[0-9]{1,2}:[0-9]{1,2}(AM|PM|am|pm){0,1}', input_string).group()
            endTime = re.findall(r"[0-9]{1,2}:[0-9]{1,2}(?:AM|PM|am|pm){0,1}", input_string)[endTime_index]
            tag = re.search(r':[A-Z]+', input_string).group()
            db_crud.create_task(date, startTime, endTime, tag, taskDescription)
        except Exception as e:
            print(e)
    #Run if deleting tasks
    elif command in deleteCommands:
        db_crud.delete_all_tasks()
    elif command in reportCommands:
        if input_string.strip().lower() in reportCommands:
            report_builder = ReportBuilder()
            report_builder.add_command("Report")
            report_command = report_builder.build()
            print(report_command.execute())
        elif len(input_string.split()) == 3:
            start_date_index = 1
            end_date_index = 2
            start_date = input_string.split()[start_date_index]
            end_date = input_string.split()[end_date_index]
            print(db_crud.format_tasks(db_crud.query_tasks_by_date_range(start_date, end_date)))
            return
        else:
            print("The report command format you entered doesn't exist. Please try again...")
            return
    #Run if querying
    elif command in queryCommands:
        #Query all tasks
        if input_string.strip().lower() in queryCommands:
            print(db_crud.format_tasks(db_crud.read_tasks()))
            return
        # Only query tasks by date range
        # elif len(input_string.split()) == 3:
        #     start_date_index = 1
        #     end_date_index = 2
        #     start_date = input_string.split()[start_date_index]
        #     end_date = input_string.split()[end_date_index]
        #     print(db_crud.format_tasks(db_crud.query_tasks_by_date_range(start_date, end_date)))
        try:
            query = re.search(r' .+', input_string).group().strip()
            # Only query tasks by description
            if query.__contains__("\"") or query.__contains__("\'"):
                query = query.replace("\"", "")
                query = query.replace("\'", "")
                print(db_crud.format_tasks(db_crud.query_tasks_by_description(query)))
            #Only query tasks by tag
            elif query.__contains__(":"):
                print(db_crud.format_tasks(db_crud.query_tasks_by_tag(query)))
            #Only query tasks by date
            else:
                query = DateHelper.convert_date_string_to_standard(query)
                print(db_crud.format_tasks(db_crud.query_tasks_by_date(query)))
        except Exception as e:
            print(e)
    else:
        print("Command: " + command + " does not exist")


if __name__ == "__main__":
    print("Whenever you want to exit please type \"exit\" or \"e\"")
    db_crud.create_tasks_table()
    while True:
        command = input("Enter your command ")
        if command == "exit" or command == "e":
            break
        parse_input_string(command)
