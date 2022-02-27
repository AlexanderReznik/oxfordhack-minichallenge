import json
import urllib.parse
import urllib.request
import requests
from thefuzz import fuzz
import sys


class Scrapper:
    def __init__(self):
        self.config = json.load(open("config.json"))

    def write_output(self, output):
        with open("output.json", "w") as output_file:
            output_file.write(json.dumps(output))

    def process_company(self, company):
        gscore = self.google_scrapper(company)
        yscore = self.yelp_scrapper(company)
        return {"name": company["name"], "rating": gscore + yscore}

    def google_scrapper(self, company):
        result = self.send_google_api_request(company["name"])
        google_score = self.get_google_score(company["name"], result) if result else 0
        return google_score

    def process(self, filename):
        data = json.load(open(filename))
        output = list(map(self.process_company, data))
        self.write_output(output)

    def get_google_score(self, name, response):
        name_similarity = fuzz.token_sort_ratio(name, response["result"]["name"])
        return self.config["coefficients"]["google"] if name_similarity > 90 else 0

    def send_google_api_request(self, name):
        api_key = open(".api_key").read()
        service_url = "https://kgsearch.googleapis.com/v1/entities:search"
        params = {
            "query": name,
            "limit": 1,
            "indent": True,
            "key": api_key,
        }
        url = service_url + "?" + urllib.parse.urlencode(params)
        response = json.loads(urllib.request.urlopen(url).read())

        return response["itemListElement"][0] if response["itemListElement"] else {}

    def yelp_scrapper(self, company):
        response = self.send_yelp_api_request(company)
        yelp_score = self.get_yelp_score(company["name"], response) if response else 0
        return yelp_score

    def get_yelp_score(self, name, response):
        name_similarity = fuzz.token_sort_ratio(name, response["name"])
        if name_similarity < 65:
            return 0
        return self.config["coefficients"]["yelp"] + self.get_review_score(
            response["review_count"]
        )

    def get_review_score(self, review_count):
        max_review_count = self.config["coefficients"]["max_review_count"]
        return (
            min(max_review_count, review_count)
            / max_review_count
            * self.config["coefficients"]["reviews"]
        )

    def send_yelp_api_request(self, company):
        MY_API_KEY = open(".yelp_api_key").read()

        headers = {"Authorization": "Bearer %s" % MY_API_KEY}
        url = "https://api.yelp.com/v3/businesses/search"
        params = {"term": company["name"], "location": company["address"]}

        response = requests.get(url, params=params, headers=headers)
        response = json.loads(response.text)
        return response["businesses"][0] if response["businesses"] else {}


if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.process(sys.argv[1])
