# pylint: skip-file
from dotenv import dotenv_values
from clapstone.models.request import APIRepository
from clapstone.models.headers import RequestHeaders
import requests
from clapstone.models.joboffer import JobOffer

envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]

repo = APIRepository("https://api.recruitee.com/c")
headers = RequestHeaders(str(recruitee_key))
repo.add_to_base_url(recruitee_company_id)

offer = JobOffer(
    title="prueba buena",
    city="socuellamos",
    description="hello world",
    requirements="java",
    postal_code="13630",
)

offer.create_payload()
payload = offer.payload

headers.add_content_type()

response = repo.post("/offers", data=payload, headers=headers.headers)
print(response.json()["offer"]["id"])
