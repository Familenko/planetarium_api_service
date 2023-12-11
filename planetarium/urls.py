from django.urls import path, include
from rest_framework import routers

from planetarium.views import ShowSessionViewSet

router = routers.DefaultRouter()
router.register("show_session", ShowSessionViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
