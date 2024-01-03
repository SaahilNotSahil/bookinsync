from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Bus, City, Route, Seat
from .serializers import (BusSerializer, CitySerializer, RouteSerializer,
                          SeatSerializer)


@login_required(login_url="/auth/login/")
def index(request):
    return render(request, "booking.html")


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]


class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [AllowAny]


class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]


class RouteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        src = request.query_params.get("src")
        dst = request.query_params.get("dst")

        if not src:
            return Response(
                {
                    "error": "Source is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        if not dst:
            return Response(
                {
                    "error": "Destination is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        routes = Route.objects.filter(
            src__name=src,
            dst__name=dst
        )

        if not routes.exists():
            return Response(
                {
                    "error": "Route not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        route = routes.first()

        buses = Bus.objects.filter(route=route).prefetch_related(
            Prefetch(
                "seats",
                queryset=Seat.objects.filter(booked=False),
                to_attr="all_seats"
            )
        )
        if not buses.exists():
            return Response(
                {
                    "error": "Bus not found for this route"
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer = BusSerializer(buses, many=True)

        return Response(
            serializer.data,
            status=HTTP_200_OK
        )


class BusAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        route_id = request.query_params.get("route_id")
        if not route_id:
            return Response(
                {
                    "error": "Route id is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        routes = Route.objects.filter(id=route_id)
        if not routes.exists():
            return Response(
                {
                    "error": "Route not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        route = routes.first()

        buses = Bus.objects.filter(route=route).prefetch_related(
            Prefetch(
                "seats",
                queryset=Seat.objects.filter(booked=False),
                to_attr="all_seats"
            )
        )

        if not buses.exists():
            return Response(
                {
                    "error": "Bus not found for this route"
                },
                status=HTTP_404_NOT_FOUND
            )

        serializer = BusSerializer(buses, many=True)

        return Response(
            serializer.data,
            status=HTTP_200_OK
        )


class BookingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bus_id = request.query_params.get("bus_id")
        if not bus_id:
            return Response(
                {
                    "error": "Bus id is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        bus = Bus.objects.filter(id=bus_id)
        if not bus:
            return Response(
                {
                    "error": "Bus not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        bus = bus.first()

        seats = Seat.objects.filter(bus_id=bus_id)
        if not seats:
            return Response(
                {
                    "error": "Bus not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "bus_id": bus_id,
                "bus_name": bus.name,
                "occupancy": bus.occupancy,
                "capacity": bus.capacity,
                "remaining_seats": bus.remaining_seats,
                "is_full": bus.is_full,
                "seats": [
                    {
                        "number": seat.number,
                        "booked": seat.booked
                    }
                    for seat in seats
                ]
            },
            status=HTTP_200_OK
        )

    @transaction.atomic
    def post(self, request):
        user = request.user

        bus_id = request.data.get("bus_id")

        if not bus_id:
            return Response(
                {
                    "error": "Bus id is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        bus = Bus.objects.filter(id=bus_id)
        if not bus:
            return Response(
                {
                    "error": "Bus not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        bus = bus.first()

        if bus.is_full:
            return Response(
                {
                    "error": "Bus is full"
                },
                status=HTTP_400_BAD_REQUEST
            )

        seat_number = request.data.get("seat_number")
        if not seat_number:
            return Response(
                {
                    "error": "Seat number is required"
                },
                status=HTTP_400_BAD_REQUEST
            )

        seat = Seat.objects.filter(
            bus=bus,
            number=seat_number
        )
        if not seat:
            return Response(
                {
                    "error": "Seat not found"
                },
                status=HTTP_404_NOT_FOUND
            )

        seat = seat.first()

        if seat.booked:
            return Response(
                {
                    "error": "Seat already booked"
                },
                status=HTTP_400_BAD_REQUEST
            )

        seat.booked = True
        seat.user = user
        seat.save()

        bus.occupancy += 1
        bus.save()

        return Response(
            {
                "success": "Seat booked successfully"
            },
            status=HTTP_200_OK
        )
