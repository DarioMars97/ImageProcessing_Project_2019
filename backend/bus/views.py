from django.http import HttpResponse
import json

def busView(request):
    bus = {"bus": 1003, "route": ["El-Haram", "El-Dokki", "El-Maniel"]}
    bus = json.dumps(bus)
    return HttpResponse(bus)
