# pylint: skip-file
from dotenv import dotenv_values
from clapstone.models.request import APIRepository
from clapstone.models.headers import RequestHeaders
import requests

envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]

repo = APIRepository("https://api.recruitee.com/c")
headers = RequestHeaders(
    {"authorization": f"Bearer {str(recruitee_key)}", "accept": "application/json"}
)
repo.add_to_base_url(recruitee_company_id)

# response = repo.get("/offers", headers.headers)

# print(response)
"""
url = "https://api.recruitee.com/c/89712/offers"

payload = {
    "offer": {
        "kind": "job",
        "remote": False,
        "title": "job 2",
        "description": "desc 1",
        "requirements": "req 1 ",
        "postal_code": "111111",
        "city": "Madrid",
        "state_code": "MAD",
        "country_code": "ES",
        "status": "published",
    }
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "authorization": "Bearer ai82cTNqTmVyZjdnZ3J3VzB5bEVUQT09",
}

response = requests.post(url, json=payload, headers=headers)
response = response.json()
print(response["offer"]["id"])
"""
