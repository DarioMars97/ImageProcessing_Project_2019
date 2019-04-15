from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus, Zone, Image
from .serializers import BusSerializer, ZoneSerializer, ImageSerializer
import json


def busView(request, format= None):
    bus = {"bus": 1003, "route": ["El-Haram", "El-Dokki", "El-Maniel"]}
    bus = json.dumps(bus)
    return HttpResponse(bus)


@api_view(['GET', 'POST'])
def busList(request, format= None):
    """
    List all Buses numbers, or create a new bus number.
    :param request:
    :return:
    """

    if request.method == 'GET':
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoneList(APIView):
    """
    List all zones , or create a new zone.
    :param request:
    :return:
    """

    def get(self, request, format=None):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUpload(APIView):
    """
    List all Images , or upload a new image.
    """

    def post(self, request, format=None):
        try:
            file = request.data['bus_image']
        except KeyError:
            return Response('Request has no resource file attached',
                            status=status.HTTP_400_BAD_REQUEST)
        Image.objects.create(image=file)
        return HttpResponse("image received", status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class BusZones(APIView):
    """
    List bus zones, or add a new zone to bus.
    """

    def get(self, request, busNo, format=None):
        bus = Bus.objects.get(bus_number=busNo)
        serializer = BusSerializer(bus)
        return Response(serializer.data)

    def post(self, request, busNo, format=None):
        zoneTxt = request.data["zone_text"]
        bus = Bus.objects.get(bus_number=busNo)

        try:
            zone = Zone.objects.get(zone_text=zoneTxt)
        except:
            zone = None

        if zone is None:
            serializer = ZoneSerializer(data=request.data)
            if serializer.is_valid() is False:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

        bus_serializer = BusSerializer(bus)
        zone_serializer = ZoneSerializer(zone)
        if zone_serializer.data in bus_serializer["zones"].data:
            return Response("Zone already in bus zones.",
                            status=status.HTTP_302_FOUND)
        bus.zones.add(zone)
        bus.save()
        return Response(bus_serializer.data, status=status.HTTP_201_CREATED)
