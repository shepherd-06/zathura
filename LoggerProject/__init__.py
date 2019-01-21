import os
import sys
import time
from datetime import datetime
from .sqlite_utility import Sqlite_Utility
from .utility import Utility
from git import Repo

def create_app():
    # It should be hardcode False on production
    known_commands = ('v', 'insert', 'get_all', 'user', 'get_debug_all', 'error_name', 'date', 'get_error_all')
    if len(sys.argv) > 1:
        for args in sys.argv[1:]:        
            if args in known_commands:
                sql_utils = Sqlite_Utility()
                if args == 'v':
                    repo = Repo(os.getcwd())
                    if repo.tags is not None:
                        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                        print(tags[-1])
                    else:
                        print("ERROR! version name not found.")
                elif args == 'insert':
                    for i in range(0, 10):
                        rows = sql_utils.insert_error_log(user="test123", error_name="No error - {}".format(i), error_description="no description", point_of_origin=create_app.__name__)
                        print("error inserted test: {}".format(rows))
                        debug_rows = sql_utils.insert_debug_log(user="test123", message_data="eiuhsodfdf bkisdjsdf jsbjlsdfd - {}".format(i), point_of_origin=create_app.__name__)
                        print("debug rows added {}".format(debug_rows))
                elif args == 'get_all':
                    all_error_logs = sql_utils.get_all_error_log()
                    all_debug_logs = sql_utils.get_all_debug_log()

                    print("All error logs")
                    print(all_error_logs)
                    print("-----------------------------")
                    print("-----------------------------")
                    print("All debug logs")
                    print(all_debug_logs)
                    print("-----------------------------")
                    print("-----------------------------")
                elif args == "get_error_all":
                    print(sql_utils.get_all_error_log())
                elif args == "get_debug_all":
                    print(sql_utils.get_all_debug_log())
                elif args == "error_name":
                    error_name = input("Enter the error_name: ")
                    result = sql_utils.get_error_by_error_name(error_name)
                    print(result)
                elif args == "user":
                    user = input("Enter a username: ")
                    logs = sql_utils.get_error_by_user(user)
                    print(logs)
                elif args == "date":
                    generated_after = input("Enter a date (limit_1): (dd/mm/yyyy format) ")
                    day, month, year = map(int, generated_after.split('/'))
                    generated_after = datetime(year, month, day, 0, 0, 0)

                    generated_before = input("Enter a date (limit_2): (dd/mm/yyyy format) ")
                    if generated_before is None or len(generated_before) == 0:
                        print("datetime.now() is using")
                        generated_before = None
                    else:
                        day, month, year = map(int, generated_before.split('/'))
                        generated_before = datetime(year, month, day, 0, 0, 0)
                    result = sql_utils.get_error_by_date_limit(generated_after, generated_before)
                    print(result)
            else:
                print("unknown command - {}".format(args))
                break