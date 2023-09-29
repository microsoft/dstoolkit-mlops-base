# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
import json
import requests
from azureml.core import Webservice


def get_webservice(ws, name):
    webservice = None
    try:
        list_webservices = Webservice.list(ws)
        for _webservice in list_webservices:
            if _webservice.name == name:
                webservice = _webservice
    except Exception as ex:
        print('Error while retrieving from webservice', ex)

    if webservice is None:
        print(f"Cannot find webservice {name}")
        sys.exit(-1)

    return webservice


def retrieve_authentication_key(webservice):
    key = None
    try:
        print("Retrieving the webservice's authentication key...")
        key = webservice.get_keys()[1]
    except Exception:
        print("The authentication key is not found for this webservice. Authentication might be disabled.")
    return key


def call_webservice(scoring_uri, sample_file_path, webservice_key=None):
    try:
        with open(sample_file_path, 'r') as sample_file:
            sample_data = sample_file.read()
        print('Calling webservice...')
        # Set the content type
        headers = {'Content-Type': 'application/json'}
        if webservice_key is not None:
            # If authentication is enabled, set the authorization header
            headers['Authorization'] = f'Bearer {webservice_key}'
        # Make the request and display the response
        resp = requests.post(scoring_uri, sample_data, headers=headers)
        return json.dumps({"result": resp.text})
    except Exception as ex:
        # return error message back to the client
        return json.dumps({"error": str(ex)})
