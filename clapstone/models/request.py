# pylint: skip-file
import requests


class APIRepository:
    def __init__(self, base_url):
        self.base_url = base_url
        self.payload = None

    def add_to_base_url(self, added):
        self.base_url = self.base_url + "/" + added

    def add_query_to_url(self, query_params):
        for value in query_params:
            self.base_url = self.base_url + "?" + query_params[value] + "=" + value + "&"
        self.base_url = self.base_url[:-1]

    def get(self, endpoint, headers=None, query_params=None, params=None):
        url = self.base_url + endpoint
        if query_params:
            for value in query_params:
                self.base_url = self.base_url + "?" + query_params[value] + "=" + str(value) + "&"
            self.base_url = self.base_url[:-1]
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        raise Exception(f"GET request to {self.base_url} returned status code {response.status_code}")

    def post(self, endpoint, data, headers=None):
        url = self.base_url + endpoint
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            return response
        raise Exception(f"POST request to {self.base_url} returned status code {response.status_code}")

    def patch(self, endpoint, data, headers=None):
        url = self.base_url + endpoint
        response = requests.patch(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        raise Exception(f"POST request to {self.base_url} returned status code {response.status_code}")

    def delete(self, endpoint, headers=None):
        url = self.base_url + endpoint
        response = requests.delete(url, headers=headers, timeout=10)
        return response

    def create_payload_sign(self, name, email):
        self.payload = {
            "title": "You were hired. Please sign the contract.",
            "subject": "Congratulations, you were hired.",
            "message": "Please sign this contract. Let me know if you have any questions.",
            "signers": [{"email_address": email, "name": name, "order": 0}],
            "cc_email_addresses": ["miguel.navarro@jobandtalent.es"],
            "file_url": ["https://www.dropbox.com/s/pnm4abl63epmj40/INDEFINIDO%20COMPLETO%2025%20OCT%2022.pdf?dl=0"],
            "metadata": {"custom_id": 1234, "custom_text": "NDA #9"},
            "signing_options": {
                "draw": True,
                "type": True,
                "upload": True,
                "phone": False,
                "default_type": "draw",
            },
            "field_options": {"date_format": "DD - MM - YYYY"},
            "test_mode": True,
        }
