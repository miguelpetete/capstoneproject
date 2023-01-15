import json
from dotenv import dotenv_values
from clapstone.models.rabbitmq import RabbitMQ
from clapstone.models.request import APIRepository
from clapstone.models.headers import RequestHeaders


rabbitmq = RabbitMQ()
envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
repo = APIRepository("https://api.recruitee.com/c")
repo.add_to_base_url(recruitee_company_id)

headers = RequestHeaders(str(recruitee_key))
response = repo.get("/candidates", headers=headers.headers)
candidates = response.json()["candidates"]


rabbit = RabbitMQ()
rabbit.channel.queue_declare(queue="send_email")

for candidate in candidates:
    email = candidate["emails"][0]
    name = candidate["name"]
    sender = {"email": email, "name": name}
    placements = candidate["placements"]
    placements = placements[0]
    if "disqualify_reason" in placements:
        sender["status"] = "rejected"
        # SEND MAIL TO REJECTED CANDIDATES
    elif placements["hired_at"] != None:
        sender["status"] = "hired"
        rabbit.send_message("", "send_email", json.dumps(sender))

print("DONE :) ")
