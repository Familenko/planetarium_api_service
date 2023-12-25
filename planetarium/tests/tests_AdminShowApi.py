from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import (
    AstronomyShow,
)

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


class AdminShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test_password",
            is_staff=True,
        )

        self.client.force_authenticate(self.user)

    def test_create_show(self):
        """Test creating a new show"""
        payload = {
            "title": "Sample astronomy show",
            "description": "Sample description",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        show = AstronomyShow.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(show, key))
