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


def handle_message(ch, method, properties, body):  # pylint: disable=invalid-name, unused-argument
    payload = json.loads(body)
    headers = RequestHeaders(str(recruitee_key))
    headers.add_content_type()
    repo.post("/candidates", data=payload, headers=headers.headers)
    print("DONE :) ")
    rabbitmq.close()


rabbitmq.consume_message("candidates", handle_message)
