# Function to parse the input string into individual components
from src import db_crud
import re
from datetime import datetime
def parse_input_string(input_string):
    #Command definition
    command = input_string.split()[0].lower()
    addCommands = ["record", "add", "create"]
    deleteCommands = ["delete", "remove"]
    queryCommands = ["query", "search"]

    #Run if adding new tasks
    if command in addCommands:
        try:
            date = input_string.split()[1]
            taskDescription = re.search(r'(\'|\")(.*?)(\'|\")', input_string).group()
            taskDescription = taskDescription.replace("\'", "")
            startTime = re.findall(r"[0-9]{1,2}:[0-9]{1,2}", input_string)[0]
            endTime = re.findall(r"[0-9]{1,2}:[0-9]{1,2}", input_string)[1]
            tag = re.search(r':[A-Z]+', input_string).group()
            db_crud.create_task(date, startTime, endTime, tag, taskDescription)
        except Exception as e:
            print(e)
    #Run if deleting tasks
    elif command in deleteCommands:
        db_crud.delete_all_tasks()
    #Run if querying
    elif command in queryCommands:
        #Query all tasks
        if input_string.strip() in queryCommands:
            print(db_crud.format_tasks(db_crud.read_tasks()))
            return
        try:
            query = re.search(r' .+', input_string).group().strip()
            #Only query tasks by description
            if query.__contains__("\"") or query.__contains__("\'"):
                query = query.replace("\"", "")
                query = query.replace("\'", "")
                print(db_crud.format_tasks(db_crud.query_tasks_by_description(query)))
            #Only query tasks by tag
            elif query.__contains__(":"):
                print(db_crud.format_tasks(db_crud.query_tasks_by_tag(query)))
            #Only query tasks by date
            else:
                query = db_crud.convert_date_string_to_standard(query)
                print(query)
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
        print(parse_input_string(command))
