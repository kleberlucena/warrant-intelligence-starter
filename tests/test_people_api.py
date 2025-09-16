import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

def test_create_person():
    api = APIClient()
    res = api.post("/api/people/", {
        "name": "Ana Souza",
        "mother_name": "Maria Souza",
        "national_id": "11122233344",
        "sex": "F"
    }, format="json")
    assert res.status_code == 201
