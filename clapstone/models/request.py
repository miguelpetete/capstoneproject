import requests


class APIRepository:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_to_base_url(self, added):
        self.base_url = self.base_url + "/" + added

    def add_query_to_url(self, query_params):
        for value in query_params:
            self.base_url = (
                self.base_url + "?" + query_params[value] + "=" + value + "&"
            )
        self.base_url = self.base_url[:-1]

    def get(self, endpoint, headers, query_params=None, params=None):
        url = self.base_url + endpoint
        if query_params:
            for value in query_params:
                self.base_url = (
                    self.base_url + "?" + query_params[value] + "=" + str(value) + "&"
                )
            self.base_url = self.base_url[:-1]
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        raise Exception(
            f"GET request to {self.base_url} returned status code {response.status_code}"
        )

    def post(self, endpoint, data, headers=None):
        url = self.base_url + endpoint
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            return response
        raise Exception(
            f"POST request to {self.base_url} returned status code {response.status_code}"
        )

    def put(self, endpoint, payload, headers=None):
        url = self.base_url + endpoint
        response = requests.put(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response
        raise Exception(
            f"POST request to {self.base_url} returned status code {response.status_code}"
        )

    def delete(self, endpoint, headers=None):
        url = self.base_url + endpoint
        response = requests.delete(url, headers=headers, timeout=10)
        return response
