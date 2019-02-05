from ZathuraProject.zathura import Zathura

class RunTest:

    def __init__(self):
        # Initiated Zathura - It will create a logger.db file and subsequent 
        # schemas
        self.zathura = Zathura()
    
    def run_error_test(self):
        # step 1: insert dummy data
        import time
        counter = 0
        for i in range(0, 50):
            rows = self.zathura.insert_error_log(user="test123", error_name="No error - {}".format(i), error_description="no description", point_of_origin=self.run_error_test.__name__, warning=2)
            counter += rows
        print("Inserted {} dummy error data.".format(counter))
    
    def run_debug_test(self):
        import time
        counter = 0
        for i in range(0, 50):
            debug_rows = self.zathura.insert_debug_log(developer="test123", message_data="eiuhsodfdf bkisdjsdf jsbjlsdfd - {}".format(i), point_of_origin=self.run_debug_test.__name__)
            counter += debug_rows
        print("Inserted {} dummy debug data.".format(counter))

    def self_destruct(self):
        import os
        try:
            os.remove('logger.db')
        except FileNotFoundError:
            print("BITE ME!")

    
if __name__ == '__main__':
    run_test = RunTest()
    run_test.run_error_test()
    run_test.run_debug_test()
    # run_test.self_destruct()