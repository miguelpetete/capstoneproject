# pylint: skip-file
import pytest
import json
import requests
import requests_mock
from clapstone.models.request import APIRepository
from dotenv import dotenv_values
from unittest import mock
from responses import *

envs = dotenv_values(".env")
basic_url_recruitee = "https://api.recruitee.com/c"
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
sign_key = envs["DROPBOX_SIGN_KEY"]
url_recruitee = basic_url_recruitee + f"/{recruitee_company_id}"
basic_url_signin = f"https://{sign_key}:@api.hellosign.com/v3"


@requests_mock.Mocker(kw="mock")
class TestRepository:
    @pytest.mark.unit
    def test_get_from_recruitee(self, **kwargs):
        kwargs["mock"].get(url_recruitee + "/candidates", text=GET_REC_RESPONSE)
        subject = APIRepository(url_recruitee)
        headers = {}
        get = subject.get("/candidates", headers=headers)
        assert get.status_code == 200
        assert len(get.json()["candidates"]) == 1
        assert get.json()["candidates"][0]["admin_id"] == 316973

    @pytest.mark.unit
    def test_post_from_recruitee(self, **kwargs):
        kwargs["mock"].post(url_recruitee + "/candidates", text=POST_REC_RESPONSE)
        subject = APIRepository(url_recruitee)
        data = {}
        post = subject.post("/candidates", data=data)
        assert post.status_code == 200
        assert len(post.json()["candidate"]) == 62
        assert post.json()["candidate"]["name"] == "Hello"
        assert post.json()["candidate"]["id"] == 46576785

    @pytest.mark.unit
    def test_patch_from_recruitee(self, **kwargs):
        kwargs["mock"].patch(url_recruitee + "/candidates/46576785", text=POST_REC_RESPONSE)
        subject = APIRepository(url_recruitee)
        data = {}
        patch = subject.patch("/candidates/46576785", data=data)
        assert patch.status_code == 200
        assert len(patch.json()["candidate"]) == 62
        assert patch.json()["candidate"]["name"] == "Hello"
        assert patch.json()["candidate"]["id"] == 46576785

    @pytest.mark.unit
    def test_delete_from_recruitee(self, **kwargs):
        kwargs["mock"].delete(url_recruitee + "/offers/1192594", text=DELETE_REC_RESPONSE)
        subject = APIRepository(url_recruitee)
        delete = subject.delete("/offers/1192594")
        assert delete.status_code == 200
        assert len(delete.json()) == 1
        assert len(delete.json()["offer"]) == 78
        assert delete.json()["offer"]["id"] == 1192594
        assert delete.json()["offer"]["city"] == "Tomelloso"

    # In this case of sign-in, we only make the test to the post of the /signature_request/send endpoint because it's the unique that we use:
    @pytest.mark.unit
    def test_post_from_signin(self, **kwargs):
        kwargs["mock"].post(basic_url_signin + "/signature_request/send", text=POST_REC_RESPONSE)
        subject = APIRepository(basic_url_signin)
        get = subject.post("/signature_request/send", data={}, headers={})
        assert get.status_code == 200
        assert len(get.json()) == 2
