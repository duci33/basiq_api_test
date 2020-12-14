import requests


class ApiService:

    def __init__(self):
        self.base_url = "https://au-api.basiq.io"

    def post(self, url, headers, data=None):

        if data is None:
            data = {}
        response = requests.post(self.base_url + url, headers=headers, json=data)
        if response.status_code in (200, 201, 202):
            return response.json()
        else:
            print(response.status_code)
            print(response.text)
            return None

    def get(self, url, headers):

        response = requests.get(self.base_url + url, headers=headers)
        if response.status_code in (200, 201, 202):
            return response.json()
        else:
            print(response.status_code)
            print(response.text)
            return None
