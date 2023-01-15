import json
from dotenv import dotenv_values
from clapstone.models.rabbitmq import RabbitMQ
from clapstone.models.request import APIRepository
from clapstone.models.headers import RequestHeaders


rabbitmq = RabbitMQ()
envs = dotenv_values(".env")
sign_key = envs["DROPBOX_SIGN_KEY"]
repo = APIRepository(f"https://{sign_key}:@api.hellosign.com/v3")


def handle_message(
    ch, method, properties, body
):  # pylint: disable=invalid-name, unused-argument
    message = json.loads(body)
    headers = RequestHeaders(str(sign_key))
    headers.add_content_type()
    if message["status"] == "hired":
        repo.create_payload_sign(message["name"], message["email"])
        response = repo.post(
            "/signature_request/send", data=repo.payload, headers=headers.headers
        )
        if response.status_code in (200, 201):
            print("MESSAGE SENT")
    rabbitmq.close()


rabbitmq.consume_message("send_email", handle_message)
