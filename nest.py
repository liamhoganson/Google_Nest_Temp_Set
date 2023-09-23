# Imports
import requests
from twilio.rest import Client
import os

client_id = os.environ.get('client_id')
project_id = os.environ.get('project_id')
client_secret = os.environ.get('client_service')
authorization_code = os.environ.get('authorization_code')
access_token = os.environ.get('access_token')
refresh_token = os.environ.get('refresh_token')
refresh_url = os.environ.get('refresh_url')
auth = os.environ.get('auth')
device_id = os.environ.get('device_id')
get_auth_url_link = os.environ.get('get_auth_url')

# Numbers
twilio_number = os.environ.get('twilio_number')
cell_number = os.environ.get('cell_number')


def refresh_token():
    refresh_url_request = requests.post(refresh_url)
    new_access_token = refresh_url_request.json()
    new_access_token = new_access_token['access_token']
    return new_access_token


def list_struct():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {}".format(refresh_token())
    }


    list_structure = requests.get(f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices", headers=headers)
    print(list_structure.json())


def get_authorization_code():
    get_auth_url = requests.get(get_auth_url_link)
    print(get_auth_url.json)



def get_access_token():
    get_access_token_url = requests.post(f"https://www.googleapis.com/oauth2/v4/token?client_id={client_id}&client_secret={client_secret}&code={authorization_code}&grant_type=authorization_code&redirect_uri=https://www.google.com")
    print(get_access_token_url.json())


def send_sms(message):
    twilio_account_sid = os.environ.get('twilio_account_sid')
    twilio_auth_token = os.environ.get('twilio_auth_token')
    twilio_client = Client(twilio_account_sid, twilio_auth_token)

    twilio_message = twilio_client.messages.create(
        body=message,
        from_=twilio_number,
        to=cell_number
    )


def set_mode():
    data = """{
        "command": "sdm.devices.commands.ThermostatMode.SetMode",
        "params": {
            "mode": "COOL"
        }
    }"""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(refresh_token())
    }

    set_mode_put = requests.post(f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices/{device_id}:executeCommand", data=data, headers=headers)
    print(set_mode_put.json())

success_msg = "Temperature was set to cool at 71 degrees."
fail_msg = "Could not set Temperature!"


def set_temp():
    set_mode()

    data = """{
        "command": "sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool",
        "params": {
            "coolCelsius": 21.66
        }
    }"""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(refresh_token())
    }

    set_mode_put = requests.post(f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices/{device_id}:executeCommand", data=data, headers=headers)
    test = (set_mode_put.json())
    print(test)
    if test == {}:
    	send_sms(success_msg)
    else:
       send_sms(fail_msg)


set_temp()
