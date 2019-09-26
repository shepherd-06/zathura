import requests
import json
import multiprocessing


def send_data(data, url):
    """
    Makes a little post request here. Will add new stuff later.
    """
    requests.post(url, data=data)


def send_data_to_bugtracker(**kwargs):
    try:
        data = {
            "project_token": kwargs["token"],
            "error_name": kwargs["name"],
            "error_description": kwargs["description"],
            "point_of_origin": kwargs["origin"]
        }

        process = multiprocessing.Process(target=send_data,
                                          args=(data, kwargs["url"]))
        process.start()
        process.join()
        return True
    except Exception as e:
        process.join()
        print("Exception -> {}".format(e))
        return False


def send_verbose_log_to_bugtracker(**kwargs):
    """
    sends the data from any calling class to server
    """
    try:
        payload = {
            "point_of_origin": kwargs["origin"],
            "log_description": kwargs["description"],
            "project_token": kwargs["project_token"]
        }
        process = multiprocessing.Process(target=send_data,
                                          args=(payload, 
                                                kwargs["bugtracker_url"]))
        process.start()
        process.join()
        return True
    except Exception as e:
        process.join()
        print("Exception occurred! : {}".format(e))
        return False
