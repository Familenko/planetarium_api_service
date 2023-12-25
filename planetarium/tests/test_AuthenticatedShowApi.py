from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers.astronomy_show import AstronomyShowDetailSerializer, AstronomyShowListSerializer

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


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
