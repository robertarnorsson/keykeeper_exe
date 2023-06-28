import os
import uuid
import json
import base64
import keyring

from constants import PROJECT_DIR, USERS_PATH
from session import Session


def abs_path(file):
    return os.path.join(PROJECT_DIR, file)

def make_uuid():
    return uuid.uuid4()

def logout():
    delete_keyring(f'KeyKeeper - {Session.USER_UUID}', Session.USER_UUID)
    Session.USER_UUID = ""
    Session.NAME = ""
    Session.FILTER = ""

def get_settings(category, section):
    with open(f'{USERS_PATH}\\{Session.USER_UUID}\\settings.json', 'r') as file:
        settings_decode = base64.b64decode(file.read()).decode()
        settings = json.loads(settings_decode)
        
        if category in settings and section in settings[category]:
            return settings[category][section]
        
    return None

def update_settings(category, section, new_value):
    with open(f'{USERS_PATH}\\{Session.USER_UUID}\\settings.json', 'r') as file:
        settings_decode = base64.b64decode(file.read()).decode()
        settings = json.loads(settings_decode)
        
    if category in settings and section in settings[category]:
        settings[category][section] = new_value
        
        with open(f'{USERS_PATH}\\{Session.USER_UUID}\\settings.json', 'w') as file:
            file.write(base64.b64encode(json.dumps(settings).encode()).decode())

def replace_settings(user_uuid, new_settings):
    new_settings['user']['uuid'] = user_uuid
    with open(f'{USERS_PATH}\\{user_uuid}\\settings.json', 'w') as file:
        settings_base64 = base64.b64encode(json.dumps(new_settings).encode()).decode()
        file.write(settings_base64)

def set_keyring(service_name: str, username: str, password_to_save: str):
    keyring.set_password(service_name, username, password_to_save)

def get_keyring(service_name: str, username: str):
    return keyring.get_password(service_name, username)

def delete_keyring(service_name: str, username: str):
    if not Session.USER_UUID:
        if keyring.get_password(service_name, 'Keykeeper - '):
            keyring.delete_password(service_name, 'Keykeeper - ')
        return
    try:
        keyring.delete_password(service_name, username)
    except:
        if Session.USER_UUID:
            print(f'Password failed to get removed from keyring/credetial manager! Please remove the password manualy.\nLook for the name: KeyKeeper - {Session.USER_UUID}')
        else:
            return

def encode_b64(string: str, encoding: str):
    string_bytes = string.encode(encoding)
    b64_bytes = base64.b64encode(string_bytes)
    b64_string = b64_bytes.decode(encoding)
    return b64_string

def decode_b64(b64_string: str, encoding: str):
    b64_string_bytes = b64_string.encode(encoding)
    b64_bytes = base64.b64decode(b64_string_bytes)
    string = b64_bytes.decode(encoding)
    return string
