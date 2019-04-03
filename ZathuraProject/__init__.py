import os
import sys
import time
import pkg_resources 
import pyfiglet
from datetime import datetime
from uuid import uuid4
from datetime import datetime
from ZathuraProject.utility import Utility
from ZathuraProject.zathura import Zathura

CURRENT_VERSION = "v0.0.4a2"
known_commands = ('v', 'developer', 'debug_origin', 'error_user', 'all_debug',
                  'error_name', 'date', 'all_error', 'origin', 'mark_resolve', 'delete_debug', 'help',)


def create_app():
    if sys.version_info < (3, 0, 0):
        print("Zathura needs python3.x to perform normally!")
        sys.exit(255)

    pyfiglet_ascii() # spits out zathura in speed font

    if len(sys.argv) > 1:
        for args in sys.argv[1:]:
            if args in known_commands:
                print("Current argument: {}".format(args))
                sql_utils = Zathura()
                if args == 'v':
                    print("*#$" * 20)
                    print("Current version: {}".format(CURRENT_VERSION))
                    print("*#$" * 20)
                elif args == "all_error":
                    filter_resolved = input(
                        "Press 1 to see all errors, including resolved, any key for others: ")
                    # filters data in descending order based on logged_at time.
                    desc = ask_filter_and_order(ask_limit=False)
                    if filter_resolved == '1':
                        print_stuff_nice_and_good(sql_utils.get_all_error_log(
                            show_all=True, desc=desc), "All Error logs")
                    else:
                        print_stuff_nice_and_good(
                            sql_utils.get_all_error_log(desc=desc), "All Error logs")
                elif args == "all_debug":
                    print_stuff_nice_and_good(
                        sql_utils.get_all_debug_log(), "All Debug messages")
                elif args == "error_name":
                    error_name = input("Enter the error_name: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    result = sql_utils.get_error_by_error_name(
                        error_name, generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(
                        result, "Errors based on error name", generated_after, generated_before, limit, desc, error_name)
                elif args == "user":
                    user = input("Enter a username: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    logs = sql_utils.get_error_by_user(
                        user, limit, desc, generated_after, generated_before)
                    print_stuff_nice_and_good(
                        logs, "Errors based on user", generated_after, generated_before, limit, desc, user)
                elif args == 'origin':
                    origin = input("Enter point of origin: ")
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    logs = sql_utils.get_error_by_origin(
                        origin, generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(
                        logs, "Errors based on origin function/class", generated_after, generated_before, limit, desc, origin)
                elif args == "date":
                    generated_after, generated_before = ask_date()
                    desc, limit = ask_filter_and_order()
                    result = sql_utils.get_error_by_date_limit(
                        generated_after, generated_before, limit, desc)
                    print_stuff_nice_and_good(
                        result, "Errors between a date frame", generated_after, generated_before, limit, desc)
                elif args == 'debug_origin':
                    origin = input("Enter <DEBUG> point of origin: ")
                    generated_after, generated_before = ask_date()
                    verbose = sql_utils.get_debug_by_origin(
                        origin, generated_after, generated_before)
                    print_stuff_nice_and_good(verbose, "Debug messages based on origin function/class",
                                              generated_after, generated_before, search_criteria=origin)
                elif args == 'developer':
                    dev = input("Enter the developers name: ")
                    generated_after, generated_before = ask_date()
                    verbose = sql_utils.get_debug_by_developers(
                        dev, generated_after, generated_before)
                    print_stuff_nice_and_good(
                        verbose, "Debug messages based on developers name", generated_after, generated_before, search_criteria=dev)
                elif args == 'mark_resolve':
                    error_name = input("Please provide error name: ")
                    origin = input("Please provide point of origin: ")
                    result = sql_utils.mark_resolve(error_name, origin)
                    print("Number of modified rows {}".format(result))
                elif args == 'delete_debug':
                    sql_utils.delete_old_debug()
                elif args == 'help':
                    command_man()
            else:
                print("unknown command - {}".format(args))
                command_man()
                break
    else:
        print("*#$" * 20)
        print("Current version: {}".format(CURRENT_VERSION))
        print("*#$" * 20)
    return


def pyfiglet_ascii():
    print(pyfiglet.figlet_format("Zathura", font="speed"))

def ask_filter_and_order(ask_limit=True):
    desc = input(
        "Do you want to filter the result in descending order? Press 1 to confirm, Press any key to continue: ")
    if desc == '1':
        desc = True
    else:
        desc = False

    if ask_limit:
        while True:
            limit = input(
                "Do you want to limit the result? Print out the number. Number must be non-zero. Press Enter to skip: ")
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
    else:
        return desc


def ask_date():
    generated_after = input(
        "Show logs after this date (inclusive) (limit_1): (dd/mm/yyyy format): ")
    if generated_after is None or len(generated_after) == 0:
        print("No date filter then")
        return (None, None)
    else:
        day, month, year = map(int, generated_after.split('/'))
        generated_after = datetime(year, month, day, 0, 0, 0)

        generated_before = input(
            "Show logs before this date (inclusive) (limit_2): (dd/mm/yyyy format): ")
        if generated_before is None or len(generated_before) == 0:
            print("Current date will be using")
            generated_before = None
        else:
            day, month, year = map(int, generated_before.split('/'))
            generated_before = datetime(year, month, day, 0, 0, 0)

        return (generated_after, generated_before)


def print_stuff_nice_and_good(payload: dict, message: str = None, date_filter_after: datetime = None, date_filter_before: datetime = None, limit: int = 0, desc: bool = False, search_criteria: str = None):
    """
    print stuff in cute and functional way for now.
    payload: dict the payload you just received from the sqlite_utility file
    message: str any extra message you want to add?
    """
    if payload is None:
        return

    if 'error' in payload:
        error_message = payload[Utility.Tag_error_message]
        print("[[[[[ Error occurred. ]]]]]\nMessage: ```{}```".format(error_message))
    else:
        os.system('clear')

    total = payload[Utility.Tag_Total] if Utility.Tag_Total in payload else None
    if total is None:
        return
    logs = payload[Utility.Tag_Log] if Utility.Tag_Log in payload else None
    if logs is None:
        return

    print('--------------------------------------------------------')
    print('--------------------------------------------------------')
    if message is not None:
        print(message)
    if search_criteria is not None:
        print("Search Criteria: {}".format(search_criteria))
    if date_filter_after is not None:
        _ = "Generated from: {}".format(
            date_filter_after.strftime(Utility.get_print_timeformat()))
        if date_filter_before is not None:
            _ += " to {}".format(date_filter_before.strftime(
                Utility.get_print_timeformat()))
        print(_)

    if limit != 0:
        print("Total result is limited to {} data only".format(limit))

    if desc:
        print("Result is in descending order")
    else:
        print("Result is in ascending order")
    print('--------------------------------------------------------')
    print("Logs found = {}".format(total))
    print('--------------------------------------------------------\n')
    
    counter = 1
    for log in logs:
        if 'error_name' in log:
            print("[[ {} ]] | User: [[ {} ]] | Error: [[ {} ]] | Warning Level: [[ {} ]] | logged at: {} | Originated at [[ {} ]]".format(
                counter, log['user'], log['error_name'], log['warning_level'], log['logged_at'], log['point_of_origin']))
            print("Error Description: {}".format(log['error_description']))
            if log['is_resolved'] == "Resolved":
                print("Status: Resolved. Resolved at {}".format(
                    log['resolved_at']))
            else:
                print("Status: Not Resolved yet")
            print('--------------------------------------------------------\n')
        else:
            print("[[ {} ]] | Developer: [[ {} ]] | logged at: {} | Location: [[ {} ]]".format(
                counter, log['user'], log['logged_at'], log['point_of_origin']))
            print("Message: {}".format(log['message-data']))
            print('--------------------------------------------------------\n')
        counter += 1


def command_man():
    """
    This is command manual. This will print out the helper function of this command.
    """
    helper = {
        'v': 'Show the current version of this package',
        'developer': 'Search based on developers name. You can filter out the result based on date and descending order',
        'debug_origin': 'Shows debug messages based on point of origin. Point of origin is the class/function from where you are adding a message in sqlite.',
        'all_debug': 'Shows all debug messages',
        'delete_debug': 'Deletes the last seven days of debug mesasges from the database. It is useful if you dont want to clutter the database with unnecessary debug info.',
        'all_error': 'Shows all error messages',
        'error_name': 'Shows error based on a error name.',
        'date': 'Shows error occurred in between a specific date.',
        'error_user': 'Shows error generated under the given username',
        'origin': 'Shows error generated on the given point of origin',
        'mark_resolve': 'Given an error name and point of origin all errors logged on database, is marked resolved.',
        'help': 'Shows all the commands necessary to run this package from terminal',
    }
    print('usage: Zathura COMMAND [args] ...')
    print(
        'For example: { Zathura v } will show the current version of this pacakge.')
    print('-----------------------------------------------------')
    print('-----------------------------------------------------')
    print("All commands: ")
    for commands in known_commands:
        print('[[ {} ]] : {}'.format(commands, helper[commands]))
    print('-----------------------------------------------------')
    print('-----------------------------------------------------')


if __name__ == '__main__':
    if sys.version_info < (3, 0, 0):
        print("Zathura needs python3.x to perform normally!")
        sys.exit(255)
    else:
        create_app()
