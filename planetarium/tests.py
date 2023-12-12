from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
)

from planetarium.serializers.astronomy_show import (
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer,
)

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample astronomy show",
        "description": "Sample description",
        "image": None,
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_show_theme(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def sample_planetarium_dome(**params):
    defaults = {
        "name": "Blue",
        "rows": 20,
        "seats_in_row": 20,
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**defaults)


def sample_show_session(**params):
    astronomy_show = AstronomyShow.objects.create(
        title="Sample astronomy show",
        description="Sample description",
    )
    planetarium_dome = PlanetariumDome.objects.create(
        name="Blue",
        rows=20,
        seats_in_row=20,
    )

    defaults = {
        "show_time": "2025-06-02 14:00:00",
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


class AnonimShowApiTests(TestCase):
    client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test_password",
        )
        self.client.force_authenticate(self.user)

    def test_detail_show(self):
        """Test retrieving a detail of show"""
        show = sample_astronomy_show()
        show.show_themes.add(sample_show_theme())
        show.show_themes.add(sample_show_theme(name="Comedy"))

        url = reverse("planetarium:astronomyshow-detail", args=[show.id])
        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(show)
        self.assertEqual(res.data, serializer.data)

    def test_list_show(self):
        show_1 = sample_astronomy_show()

        show_theme = sample_show_theme()
        show_theme_2 = sample_show_theme(name="Comedy")

        show_1.show_themes.add(show_theme)
        show_1.show_themes.add(show_theme_2)

        show_2 = sample_astronomy_show(
            title="Sample astronomy show 2",
            description="Sample description 2",
        )
        show_2.show_themes.add(show_theme)
        show_2.show_themes.add(show_theme_2)

        res = self.client.get(ASTRONOMY_SHOW_URL)

        serializer1 = AstronomyShowListSerializer(show_1)
        serializer2 = AstronomyShowListSerializer(show_2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)


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
