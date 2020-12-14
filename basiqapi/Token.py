import time
import config
from ApiService import ApiService


class Token:

    def __init__(self):
        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.updated_at = None
        self.api_service = ApiService()

    def get_access_token(self):

        if self.expires_in and time.time() - self.updated_at < self.expires_in:
            return self.access_token
        else:
            headers = {"Authorization": "Basic " + config.API_KEY, "Content-Type": "application/x-www-form-urlencoded",
               "basiq-version": "2.0", "scope": "SERVER_ACCESS"}
            res = self.api_service.post("/token", headers)
            if res:
                self.access_token = res["access_token"]
                self.token_type = res["token_type"]
                self.expires_in = res["expires_in"]
                self.updated_at = time.time()
                return self.access_token
            else:
                print("Token is None")
                return None
