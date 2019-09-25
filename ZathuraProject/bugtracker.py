import requests
import json

def send_data_to_bugtracker(name: str, description: str, origin: str, token: str, url: str):
    try:
        data = {
            "project_token": token,
            "error_name": name,
            "error_description": description,
            "point_of_origin": origin
        }
        requests.post(url, data=data)
    except Exception as e:
        print("Exception khaise. {}".format(e))