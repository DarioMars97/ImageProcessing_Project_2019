from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus, Zone, Image
from .serializers import BusSerializer, ZoneSerializer, ImageSerializer
import json
from .Train_Test import detect_numbers


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
        try:
            bus = Bus.objects.get(bus_number=request.data["bus_number"])
        except:
            bus = None

        try:
            link = request.data["link"]
        except:
            link = None


        if bus is not None:
            if link is not None:
                bus.link = link
                bus.save()
            bus_serializer = BusSerializer(bus)
            return Response(bus_serializer.data, status=status.HTTP_201_CREATED)
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
        try:
            zone = Zone.objects.get(zone_text=request.data["zone_text"])
        except:
            zone = None

        if zone is not None:
            return Response("zone found!", status=status.HTTP_304_NOT_MODIFIED)
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
        file_data = False
        string_data = False
        try:
            file = request.data['bus_image']
            file_data = True
        except KeyError:
            try:
                text = request.data['bus_image_bytes']
                string_data = True
            except KeyError:
                try:
                    file = request.body
                    file = json.loads(file)
                    text = file["bus_image_bytes"]
                    string_data = True
                except KeyError:
                    return Response('Request has no resource file attached',
                                status=status.HTTP_400_BAD_REQUEST)
        the_returned = None
        if file_data:
            Image.objects.create(image=file)
            the_returned = detect_numbers(file_data=file_data)
        elif string_data:
            Image.objects.create(text=text)
            the_returned = detect_numbers(string_data=string_data)
        else:
            return HttpResponse("upload error", status=status.HTTP_400_BAD_REQUEST)
        # print(the_returned)
        try:
            bus = Bus.objects.get(bus_number=the_returned)
        except:
            bus = None

        if bus is None:
            # return Response("Bus is not found in our database please inform us urgently",
            #                 status=status.HTTP_404_NOT_FOUND)
            serializer = BusSerializer(data={"bus_number": the_returned})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = BusSerializer(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class BusZones(APIView):
    """
    List bus zones, or add a new zone to bus.
    """

    def get(self, request, busNo, format=None):
        try:
            bus = Bus.objects.get(bus_number=busNo)
        except:
            bus = None

        if bus is None:
            return Response("Bus is not found", status=status.HTTP_404_NOT_FOUND)

        serializer = BusSerializer(bus)
        return Response(serializer.data)

    def post(self, request, busNo, format=None):
        try:
            zoneTxt = request.data["zone_text"]
        except:
            zoneTxt = None

        try:
            link = request.data["link"]
        except:
            link = None

        try:
            bus = Bus.objects.get(bus_number=busNo)
        except:
            bus = None

        if bus is None:
            bus_serializer = BusSerializer(data={"bus_number": busNo})
            if bus_serializer.is_valid() is False:
                return Response(bus_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            bus_serializer.save()
        else:
            bus_serializer = BusSerializer(bus)
        bus = Bus.objects.get(bus_number=busNo)

        try:
            zone = Zone.objects.get(zone_text=zoneTxt)
        except:
            zone = None

        if link is not None:
            bus.link = link

        if zoneTxt is not None:
            if zone is None:
                zone_serializer = ZoneSerializer(data=request.data)
                if zone_serializer.is_valid() is False:
                    return Response(zone_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
                zone_serializer.save()
            else:
                zone_serializer = ZoneSerializer(zone)

            zone = Zone.objects.get(zone_text=zoneTxt)

            if zone_serializer.data in bus_serializer["zones"].data:
                return Response("Zone already in bus zones.",
                                status=status.HTTP_302_FOUND)
            bus.zones.add(zone)
        bus.save()
        bus_serializer = BusSerializer(bus)
        return Response(bus_serializer.data, status=status.HTTP_201_CREATED)
