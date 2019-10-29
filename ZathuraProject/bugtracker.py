import requests
import json


def send_data(data, url):
    """
    sends data to bugtracker (local deployment) using requests package.
    """
    return requests.post(url, data=data)


def send_data_to_bugtracker(**kwargs):
    """
    sends error log to bugtracker. 
    mandatory parameters: url, token, name, description and origin
    optional parameters: user.
    """
    try:
        data = {
            "project_token": kwargs["token"],
            "error_name": kwargs["name"],
            "error_description": kwargs["description"],
            "point_of_origin": kwargs["origin"]
        }
        if kwargs["user"] is not None:
            data["identifier"] = kwargs["user"]

        response = send_data(data, kwargs["url"])
        if response.status_code != 200:
            print("--------------------------------")
            print(response.text)
            print("--------------------------------\n\n")
            return False
        return True
    except Exception as e:
        print("Exception -> {}".format(e))
        return False


def send_verbose_log_to_bugtracker(**kwargs):
    """
    sends verbose log to bugtracker server
    mandatory parameters: url, project_token, description and origin
    optional parameters: user.
    """
    try:
        payload = {
            "point_of_origin": kwargs["origin"],
            "log_description": kwargs["description"],
            "project_token": kwargs["project_token"]
        }
        if kwargs["user"] is not None:
            payload["identifier"] = kwargs["user"]
        response = send_data(payload, kwargs["bugtracker_url"])
        if response.status_code != 200:
            print("--------------------------------")
            print(response.text)
            print("--------------------------------\n\n")
            return False
        return True
    except Exception as e:
        print("Exception occurred! : {}".format(e))
        return False
