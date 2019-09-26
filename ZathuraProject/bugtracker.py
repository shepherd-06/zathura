import requests
import json


def send_data_to_bugtracker(**kwargs):
    try:
        data = {
            "project_token": kwargs["token"],
            "error_name": kwargs["name"],
            "error_description": kwargs["description"],
            "point_of_origin": kwargs["origin"]
        }
        requests.post(kwargs["url"], data=data)
        return True
    except Exception as e:
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
        requests.post(kwargs["bugtracker_url"], data=payload)
        return True
    except Exception as e:
        print("Exception occurred! : {}".format(e))
        return False
