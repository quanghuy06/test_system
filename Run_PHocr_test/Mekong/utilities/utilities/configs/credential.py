import os
import json
import base64

class Credential:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.config_file = os.path.join(script_dir, "account/credential.json")

        with open(self.config_file) as f:
            self.data = json.load(f)

    def get_account_for(self, key):
        user = self.data[key]["username"]
        encoded_password = self.data[key]["password"]
        password = base64.b64decode(encoded_password)

        return user, password
