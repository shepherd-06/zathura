import os
import sys
import time
from datetime import datetime
from .sqlite_utility import Sqlite_Utility
from .utility import Utility
from git import Repo

def create_app():
    # It should be hardcode False on production
    known_commands = ('v', 'insert_test', 'dev_user', 'debug_origin', 'error_user', 'debug_all', 'error_name', 'date', 'error_all', 'origin', 'mark_resolve')
    if len(sys.argv) > 1:
        for args in sys.argv[1:]:        
            if args in known_commands:
                print("Current argument: {}".format(args))
                sql_utils = Sqlite_Utility()
                if args == 'v':
                    # TODO: is not gonna work for pip project.
                    repo = Repo(os.getcwd())
                    if get_current_version() is None:
                        print("ERROR! version name not found.")
                elif args == 'insert_test':
                    for i in range(0, 10):
                        rows = sql_utils.insert_error_log(user="test123", error_name="No error - {}".format(i), error_description="no description", point_of_origin=create_app.__name__)
                        print("error inserted test: {}".format(rows))
                        debug_rows = sql_utils.insert_debug_log(developer="test123", message_data="eiuhsodfdf bkisdjsdf jsbjlsdfd - {}".format(i), point_of_origin=create_app.__name__)
                        print("debug rows added {}".format(debug_rows))
                elif args == "error_all":
                    print_stuff_nice_and_good(sql_utils.get_all_error_log(), "All Error logs")
                elif args == "debug_all":
                    print_stuff_nice_and_good(sql_utils.get_all_debug_log(), "All Debug messages")
                elif args == "error_name":
                    error_name = input("Enter the error_name: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    result = sql_utils.get_error_by_error_name(error_name, generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(result, "Errors based on error name", generated_after, generated_before, limit, desc, error_name)
                elif args == "user":
                    user = input("Enter a username: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    logs = sql_utils.get_error_by_user(user, limit, desc, generated_after, generated_before)
                    print_stuff_nice_and_good(logs, "Errors based on user", generated_after, generated_before, limit, desc, user)
                elif args == 'origin':
                    origin = input("Enter point of origin: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    logs = sql_utils.get_error_by_origin(origin, generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(logs, "Errors based on origin function/class", generated_after, generated_before, limit, desc, origin)
                elif args == "date":
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    result = sql_utils.get_error_by_date_limit(generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(result, "Errors between a date frame", generated_after, generated_before, limit, desc)
                elif args == 'debug_origin':
                    origin = input("Enter <DEBUG> point of origin: ")
                    generated_after, generated_before = ask_date()
                    verbose = sql_utils.get_debug_by_origin(origin, generated_after, generated_before)
                    print_stuff_nice_and_good(verbose, "Debug messages based on origin function/class", generated_after, generated_before, search_criteria=origin)
                elif args == 'dev_user':
                    dev = input("Enter the developers name: ")
                    generated_after, generated_before = ask_date()
                    verbose = sql_utils.get_debug_by_developers(dev, generated_after, generated_before)
                    print_stuff_nice_and_good(verbose, "Debug messages based on developers name", generated_after, generated_before, search_criteria=dev)
                elif args == 'mark_resolve':
                    error_name = input("Please provide error name: ")
                    origin = input("Please provide point of origin: ")
                    result = sql_utils.mark_resolve(error_name, origin)
                    print("Number of modified rows {}".format(result))
            else:
                print("unknown command - {}".format(args))
                print("All commands - {}".format(known_commands))
                break
    else:
        get_current_version()
        
def get_current_version():
    repo = Repo(os.getcwd())
    if repo.tags is not None:
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        print(tags[-1])
    else:
        return None

def ask_filter_and_order():
    desc = input("Do you want to filter the result in descending order? Press 1 to confirm, Press any key to continue: ")
    if desc == '1':
        desc = True
    else:
        desc = False

    while True:
        limit = input("Do you want to limit the result? Print out the number. Number must be non-zero. Press Enter to skip: ")
        try:
            if len(limit) == 0:
                return (desc, 0)
            limit = int(limit)
            if limit < 1:
                print("Limit must be greater than or equal to 1")
            else:
                return (desc, limit)
        except:
            pass
        

    
def ask_date():
    generated_after = input("Show logs after this date (inclusive) (limit_1): (dd/mm/yyyy format): ")
    if generated_after is None or len(generated_after) == 0:
        print("No date filter then")
        return (None, None)
    else:
        day, month, year = map(int, generated_after.split('/'))
        generated_after = datetime(year, month, day, 0, 0, 0)

        generated_before = input("Show logs before this date (inclusive) (limit_2): (dd/mm/yyyy format): ")
        if generated_before is None or len(generated_before) == 0:
            print("Current date will be using")
            generated_before = None
        else:
            day, month, year = map(int, generated_before.split('/'))
            generated_before = datetime(year, month, day, 0, 0, 0)
        
        return (generated_after, generated_before)


def print_stuff_nice_and_good(payload:dict, message: str = None, date_filter_after: datetime = None, date_filter_before: datetime = None, limit: int = 0, desc: bool = False, search_criteria: str = None):
    """
    print stuff in cute and functional way for now.
    payload: dict the payload you just received from the sqlite_utility file
    message: str any extra message you want to add?
    """
    os.system('clear')
    if payload is None:
        return
    total = payload['total'] if 'total'in payload else None
    if total is None:
        return
    logs = payload['log'] if 'log' in payload else None 
    if logs is None:
        return

    print('--------------------------------------------------------')
    print('--------------------------------------------------------')
    if message is not None:
        print(message)
    if search_criteria is not None:
        print("Search Criteria: {}".format(search_criteria))
    if date_filter_after is not None:
        _ = "Generated from: {}".format(date_filter_after.strftime(Utility.get_print_timeformat()))
        if date_filter_before is not None:
            _ += " to {}".format(date_filter_before.strftime(Utility.get_print_timeformat()))
        print(_)
    
    if limit != 0:
        print("Total result is limited into {}".format(limit))

    if desc:
        print("Result is in descending order")
    else:
        print("Result is in ascending order")
    print('--------------------------------------------------------')
    print("Logs found = {}".format(total))
    print('--------------------------------------------------------\n')

    for log in logs:
        if 'error_name' in log:
            print("User: [[ {} ]] | Error: [[ {} ]] | logged at: {} | Originated at [[ {} ]]".format(log['user'], log['error_name'], log['logged_at'], log['point_of_origin']))
            print("Error Description: {}".format(log['error_description']))
            if log['is_resolved'] == "Resolved":
                print("Status: Resolved. Resolved at {}".format(log['resolved_at']))
            else:
                print("Status: Not Resolved yet")
            print('--------------------------------------------------------\n')
        else:
            print("Developer: [[ {} ]] | logged at: {} | Location: [[ {} ]]".format(log['user'], log['logged_at'], log['point_of_origin']))
            print("Message: {}".format( log['message-data']))
            print('--------------------------------------------------------\n')
