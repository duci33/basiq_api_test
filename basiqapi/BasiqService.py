import time
from Token import Token
from ApiService import ApiService


class BasiqService:
    def __init__(self):
        self.token = Token()
        self.api_service = ApiService()

    def get_average_spending_per_category(self):

        if self.token:
            user = self.create_user()
            if user:
                connection = self.create_connection(user["id"])
                if connection:
                    jobs = self.get_jobs("/jobs/" + connection["id"])
                    if jobs:
                        transactions = self.get_transactions(None, user["id"])
                        if transactions:
                            result = self.calculate_average_amount(transactions)
                            for v in result.values():
                                print("Average spending value for '" + v["title"] + "' is " + str(round(v["avg"], 2)))

    def create_user(self):
        headers = {"Authorization": "Bearer " + self.token.get_access_token(),
                   "Content-Type": "application/json"}
        user_data = {"email": "gavin@hooli.com", "mobile": "+61410888666"}
        return self.api_service.post("/users", headers, user_data)

    def create_connection(self, user_id):
        url = "/users/" + user_id + "/connections"
        headers = {"Authorization": "Bearer " + self.token.get_access_token(),
                   "Content-Type": "application/json"}
        connection_data = {
          "loginId": "gavinBelson",
          "password": "hooli2016",
          "institution": {
            "id": "AU00000"
          }
        }
        return self.api_service.post(url, headers, connection_data)

    def get_jobs(self, url):
        headers = {"Authorization": "Bearer " + self.token.get_access_token()}
        response = self.api_service.get(url, headers)
        if not self.check_jobs_status(response):
            time.sleep(10)
            return self.get_jobs(url)
        return response

    @staticmethod
    def check_jobs_status(jobs):
        is_success = True
        for s in jobs["steps"]:
            if s["status"] != "success":
                is_success = False
                break
        return is_success

    def get_transactions(self, url, user_id):
        headers = {"Authorization": "Bearer " + self.token.get_access_token()}
        if url is None:
            url = "/users/" + user_id + "/transactions"
        transactions = self.api_service.get(url, headers)
        if transactions:
            if transactions["links"] and "next" in transactions["links"].keys():
                next_link = transactions["links"]["next"]
                next_link = next_link[next_link.index("users") - 1:]
                transactions["data"] += self.get_transactions(next_link, None)
        return transactions["data"]

    @staticmethod
    def calculate_average_amount(transactions):
        result = {}
        for t in transactions:
            id = t["subClass"]["code"]
            if id in result.keys():
                result[id]["sum"] += abs(float(t["amount"]))
                result[id]["count"] += 1
                result[id]["avg"] = result[id]["sum"]/result[id]["count"]
            else:
                result[id] = {"sum": abs(float(t["amount"])),
                              "count": 1,
                              "avg": abs(float(t["amount"]))/1,
                              "title": t["subClass"]["title"]}
        return result


if __name__ == '__main__':
    BasiqService().get_average_spending_per_category()
