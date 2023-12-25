from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


class AnonimShowApiTests(TestCase):
    client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
