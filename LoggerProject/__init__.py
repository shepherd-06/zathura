import os
import sys
from datetime import datetime
from .utility import Utility
from git import Repo

def create_app():
    # It should be hardcode False on production
    known_commands = ('v', 'db_insert', 'db_get_all', 'db_user')
    if len(sys.argv) > 1:
        for args in sys.argv[1:]:        
            if args in known_commands:
                if args == 'v':
                    repo = Repo(os.getcwd())
                    if repo.tags is not None:
                        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                        print(tags[-1])
                    else:
                        print("ERROR! version name not found.")
                elif args == 'db_insert':
                    from .sqlite_utility import Sqlite_Utility
                    import time
                    sql_utils = Sqlite_Utility()    
                    for i in range(0, 10):
                        rows = sql_utils.insert_error_log(user="test123", error_name="No error - {}".format(i), error_description="no description", point_of_origin=create_app.__name__)
                        print("error inserted test: {}".format(rows))
                        debug_rows = sql_utils.insert_debug_log(user="test123", message_data="eiuhsodfdf bkisdjsdf jsbjlsdfd - {}".format(i), point_of_origin=create_app.__name__)
                        print("debug rows added {}".format(debug_rows))
                        # time.sleep(1)
                elif args == 'db_get_all':
                    from .sqlite_utility import Sqlite_Utility
                    sql_utils = Sqlite_Utility()
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
                elif args == "db_user":
                    from .sqlite_utility import Sqlite_Utility
                    sql_utils = Sqlite_Utility()
                    before = True
                    user = input("Enter a username: ")
                    anything_else = input("Do you have anyother input left?:y to continue ")
                    if anything_else == 'y':
                        generated_after = input("Enter a date: (dd/mm/yyyy format) ")
                        day, month, year = map(int, generated_after.split('/'))
                        generated_after = datetime(year, month, day, 0, 0, 0)
                        print("Show log before or after?")
                        before_or_after = input("Press 1 for after or anyother key for before: ")
                        if before_or_after == "1":
                            before = False
                        print("Generating after {}".format(generated_after))
                    else:
                        generated_after = None
                    logs = sql_utils.get_error_by_user(user, generated_before=generated_after, before=before)
                    print(logs)
            else:
                print("unknown command - {}".format(args))
                break