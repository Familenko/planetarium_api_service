from django.shortcuts import render
from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Reservation, Ticket
from planetarium.serializers.astronomy_show import AstronomyShowSerializer, AstronomyShowListSerializer, \
    AstronomyShowDetailSerializer, AstronomyShowImageSerializer
from planetarium.serializers.planetarium_dome import PlanetariumDomeSerializer
from planetarium.serializers.reservation import ReservationSerializer, ReservationListSerializer

from planetarium.serializers.show_session import (
    ShowSessionListSerializer,
    ShowSessionDetailSerializer,
    ShowSessionSerializer,
)
from planetarium.serializers.show_theme import ShowThemeSerializer, ShowThemeListSerializer, ShowThemeDetailSerializer
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related(
        "astronomy_show", "planetarium_dome"
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        date = self.request.query_params.get("date")
        show_id = self.request.query_params.get("show_id")
        show_name = self.request.query_params.get("show_name")

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if show_id:
            queryset = queryset.filter(astronomy_show_id=show_id)

        if show_name:
            queryset = queryset.filter(astronomy_show__title__icontains=show_name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer

        if self.action == "retrieve":
            return ShowSessionDetailSerializer

        return ShowSessionSerializer


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AstronomyShow.objects.all().prefetch_related("show_themes")
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowDetailSerializer

        if self.action == "upload_image":
            return AstronomyShowImageSerializer

        return AstronomyShowSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowThemeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        show_id = self.request.query_params.get("show_id")
        show_name = self.request.query_params.get("show_name")

        if show_id:
            queryset = queryset.filter(astronomy_show_id=show_id)

        if show_name:
            queryset = queryset.filter(astronomy_show__title__icontains=show_name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowThemeListSerializer

        if self.action == "retrieve":
            return ShowThemeDetailSerializer

        return ShowThemeSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets",
        "tickets__show_session",
        "tickets__show_session__astronomy_show",
        "tickets__show_session__planetarium_dome",
    )

    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
