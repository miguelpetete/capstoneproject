# pylint: skip-file
import pytest
import json
import requests
import requests_mock
from clapstone.models.request import APIRepository
from dotenv import dotenv_values
from unittest import mock

envs = dotenv_values(".env")
basic_url_recruitee = "https://api.recruitee.com/c"
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
url_recruitee = basic_url_recruitee + f"/{recruitee_company_id}"
GET_REC_RESPONSE = """
    {
  "candidates": [
    {
      "admin_id": 316973,
      "adminapp_url": "https://app.recruitee.com/#/dashboard/overview?candidate=46566917&company=89712",
      "created_at": "2023-01-15T12:01:10.725552Z",
      "emails": [
        "mikinavarrito@gmail.com"
      ],
      "example": false,
      "followed": false,
      "has_avatar": false,
      "id": 46566917,
      "initials": "MA",
      "last_message_at": null,
      "my_last_rating": null,
      "my_pending_result_request": false,
      "my_upcoming_event": false,
      "name": "Miguel angel Navarro  arenas",
      "notes_count": 0,
      "pending_result_request": false,
      "phones": [],
      "photo_thumb_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/candidates/46566917/thumb_photo_vwd41augkyr4.png",
      "placements": [
        {
          "candidate_id": 46566917,
          "created_at": "2023-01-15T12:01:11.751937Z",
          "hired_at": "2023-01-15T12:02:22.855492Z",
          "hired_by_id": 316973,
          "hired_in_other_placement": false,
          "hired_in_this_placement": false,
          "id": 49384947,
          "job_starts_at": null,
          "language": null,
          "offer_id": 1192594,
          "overdue_at": null,
          "overdue_diff": null,
          "position": 1,
          "positive_ratings": null,
          "ratings": {},
          "stage_id": 8080464,
          "updated_at": "2023-01-15T12:02:22.863156Z"
        }
      ],
      "positive_ratings": null,
      "rating": 0,
      "ratings": {},
      "ratings_count": 0,
      "referrer": null,
      "source": "manual",
      "tasks_count": 0,
      "unread_notifications": false,
      "upcoming_event": false,
      "updated_at": "2023-01-15T12:01:10.725552Z",
      "viewed": false
    }
  ],
  "generated_at": "2023-01-15T18:13:26.613622Z",
  "references": [
    {
      "department_id": null,
      "guid": "mg62k",
      "id": 1192594,
      "kind": "job",
      "lang_code": "en",
      "location": "Tomelloso, Spain",
      "position": 8,
      "slug": "peon-de-albanil",
      "status": "published",
      "title": "Peon de albañil",
      "type": "Offer"
    },
    {
      "category": "hire",
      "created_at": null,
      "fair_evaluations_enabled": false,
      "group": null,
      "id": 8080464,
      "locked": false,
      "name": "Hired",
      "placements_count": null,
      "position": 5,
      "time_limit": null,
      "type": "Stage",
      "updated_at": null
    },
    {
      "email": "miguel.navarro@jobandtalent.com",
      "first_name": "Miguel ángel",
      "has_avatar": false,
      "id": 316973,
      "initials": "MÁ",
      "last_name": "Navarro arenas",
      "photo_normal_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/316973/normal_avatar_e5lpvmegbw9k.png",
      "photo_thumb_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/316973/thumb_avatar_e5lpvmegbw9k.png",
      "time_format24": true,
      "timezone": "Europe/Madrid",
      "type": "Admin"
    }
  ]
}
"""

POST_REC_RESPONSE = """
{
  "candidate": {
    "cv_url": null,
    "placements": [],
    "unread_notifications": false,
    "cover_letter": null,
    "adminapp_url": "https://app.recruitee.com/#/dashboard/overview?candidate=46576785&company=89712",
    "admin_ids": [],
    "my_pending_result_request": false,
    "sourcing_origin": null,
    "gdpr_status": "no_consent",
    "has_avatar": false,
    "links": [],
    "gdpr_consent_request_completed_at": null,
    "custom_fields": [],
    "referrer": null,
    "source": "manual",
    "grouped_open_question_answers": [],
    "emails": [],
    "id": 46576785,
    "referral_referrers_ids": [],
    "created_at": "2023-01-15T19:25:56.272335Z",
    "updated_at": "2023-01-15T19:25:56.272335Z",
    "fields": [
      {
        "fixed": true,
        "id": null,
        "kind": "education",
        "origin": "manual",
        "values": [],
        "visibility": {
          "admin_ids": [],
          "level": "public",
          "role_ids": []
        },
        "visible": true
      },
      {
        "fixed": true,
        "id": null,
        "kind": "experience",
        "origin": "manual",
        "values": [],
        "visibility": {
          "admin_ids": [],
          "level": "public",
          "role_ids": []
        },
        "visible": true
      }
    ],
    "gdpr_expires_at": null,
    "my_last_rating": null,
    "attachments_count": 0,
    "name": "Hello",
    "rating": 0,
    "notes_count": 0,
    "photo_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/candidates/46576785/normal_photo_yolw7pak6c9m.png",
    "photo_thumb_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/candidates/46576785/thumb_photo_yolw7pak6c9m.png",
    "open_question_answers": [],
    "gdpr_consent_ever_given": false,
    "example": false,
    "my_upcoming_event": false,
    "admin_id": 316973,
    "ratings": {},
    "tasks_count": 0,
    "rating_visible": true,
    "initials": "H",
    "cv_original_url": null,
    "online_data": null,
    "last_message_at": null,
    "viewed": false,
    "upcoming_event": false,
    "gdpr_consent_request_sent_at": null,
    "gdpr_scheduled_to_delete_at": null,
    "sourcing_data": null,
    "duplicates": [],
    "followed": false,
    "pending_request_link": false,
    "ratings_count": 0,
    "gdpr_consent_request_type": null,
    "cv_processing_status": "ok",
    "social_links": [],
    "tags": [],
    "pending_result_request": false,
    "positive_ratings": null,
    "in_active_share": false,
    "mailbox_messages_count": 0,
    "last_activity_at": "2023-01-15T19:25:56.272335Z",
    "phones": [],
    "sources": []
  },
  "references": [
    {
      "email": "miguel.navarro@jobandtalent.com",
      "first_name": "Miguel ángel",
      "has_avatar": false,
      "id": 316973,
      "initials": "MÁ",
      "last_name": "Navarro arenas",
      "photo_normal_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/316973/normal_avatar_e5lpvmegbw9k.png",
      "photo_thumb_url": "https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/316973/thumb_avatar_e5lpvmegbw9k.png",
      "time_format24": true,
      "timezone": "Europe/Madrid",
      "type": "Admin"
    }
  ]
}
"""

DELETE_REC_RESPONSE = """
{
  "offer": {
    "guid": "mg62k",
    "city": "Tomelloso",
    "category": null,
    "disqualified_candidates_count": 0,
    "qualified_candidates_count": 1,
    "pipeline": false,
    "status": "published",
    "adminapp_url": "https://app.recruitee.com/#/offers/peon-de-albanil",
    "location": "Tomelloso, Spain",
    "postal_code": "13630",
    "state_code": "MAD",
    "options_photo": "optional",
    "title": "Peon de albañil",
    "open_question_template_id": null,
    "pipeline_template_id": 654486,
    "salary": {
      "currency": null,
      "max": null,
      "min": null,
      "period": null
    },
    "education": null,
    "number_of_openings": null,
    "has_additional_info": false,
    "has_active_campaign": false,
    "id": 1192594,
    "created_at": "2023-01-15T11:12:01.569264Z",
    "email_confirmation_subject": "[job_offer] - Confirmation of your application",
    "updated_at": "2023-01-15T12:01:11.769469Z",
    "position": 8,
    "department": null,
    "fields": [],
    "employment_type": null,
    "attachments_count": 0,
    "fieldset": {
      "default": true,
      "fields": [
        {
          "id": 108113864,
          "kind": "language_skill",
          "name": null,
          "options": {},
          "visibility": {
            "admin_ids": [],
            "level": "public",
            "role_ids": []
          },
          "visible": true
        },
        {
          "id": 108113865,
          "kind": "skills",
          "name": null,
          "options": {},
          "visibility": {
            "admin_ids": [],
            "level": "public",
            "role_ids": []
          },
          "visible": true
        }
      ],
      "id": 169119,
      "name": "Basic"
    },
    "remote": false,
    "recruiter_id": null,
    "notes_count": 0,
    "job_scheduler": null,
    "slug": "peon-de-albanil",
    "hired_candidates_without_openings_count": null,
    "department_id": null,
    "mailbox_email": "job.mg62k@petete.recruitee.com",
    "followers": [],
    "min_hours": 30,
    "description": "Necesario peon de albañil en obra en Tomelloso",
    "example": false,
    "fieldset_id": 169119,
    "experience": null,
    "pipeline_template": {
      "category": null,
      "custom": false,
      "default": true,
      "id": 654486,
      "position": null,
      "requires_adjustment": false,
      "stages": [
        {
          "action_templates": [],
          "category": "referred",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080457,
          "locked": true,
          "name": "Referred",
          "placements_count": 0,
          "position": -3,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "sourced",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080458,
          "locked": true,
          "name": "Sourced",
          "placements_count": 0,
          "position": -2,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "apply",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080459,
          "locked": true,
          "name": "Applied",
          "placements_count": 0,
          "position": -1,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "phone_screen",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080460,
          "locked": false,
          "name": "Phone interview",
          "placements_count": 0,
          "position": 1,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "interview",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080461,
          "locked": false,
          "name": "On-site interview",
          "placements_count": 0,
          "position": 2,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "evaluation",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080462,
          "locked": false,
          "name": "Evaluation",
          "placements_count": 0,
          "position": 3,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "offer",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080463,
          "locked": false,
          "name": "Offer",
          "placements_count": 0,
          "position": 4,
          "time_limit": null
        },
        {
          "action_templates": [],
          "category": "hire",
          "fair_evaluations_enabled": false,
          "group": null,
          "id": 8080464,
          "locked": false,
          "name": "Hired",
          "placements_count": 0,
          "position": 5,
          "time_limit": null
        }
      ],
      "title": "Default"
    },
    "max_hours": 40,
    "primary_lang_code": "en",
    "eeo_settings": null,
    "options_cover_letter": "optional",
    "hired_candidates_count": 0,
    "state_name": null,
    "lang_code": "en",
    "issues": {
      "is_required_data_filled": false,
      "is_requisition_present": false
    },
    "email_confirmation": true,
    "kind": "job",
    "visibility_options": [
      "linkedin",
      "indeed",
      "social_share",
      "job_location"
    ],
    "closed_at": null,
    "url": "https://petete.recruitee.com/o/peon-de-albanil",
    "sharing_title": null,
    "email_confirmation_body": "<div>Your application for the [job_offer] position has been successfully submitted.</div><br><div>If you want to add something to your application just respond to this email.</div><div><br></div>[company]",
    "options_cv": "required",
    "shared_openings_count": null,
    "street": null,
    "sharing_description": null,
    "followed": false,
    "country_code": "ES",
    "careers_url": "https://petete.recruitee.com/o/peon-de-albanil",
    "admins": [],
    "options_phone": "required",
    "offer_tags": [],
    "enabled_for_referrals": false,
    "default_translations": {
      "email_confirmation_body": "<div>Your application for the [job_offer] position has been successfully submitted.</div><br><div>If you want to add something to your application just respond to this email.</div><div><br></div>[company]",
      "email_confirmation_subject": "[job_offer] - Confirmation of your application",
      "title": "Peon de albañil"
    },
    "sharing_image": null,
    "hiring_manager_id": null,
    "candidates_count": 1,
    "requirements": "Al menos un graduado escolar. Curso 20 horas albañilería",
    "auto_reply_template_id": 567833,
    "published_at": "2023-01-15T11:12:01.396647Z"
  }
}
"""


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
