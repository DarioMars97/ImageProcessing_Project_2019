from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('example', views.busView, name="bus_example"),
    path('buses', views.busList, name="bus_list"),
    path('zones', views.ZoneList.as_view(), name="zone_list"),
    path('upload_image', views.ImageUpload.as_view(), name="image_upload"),
    path('bus/<int:busNo>/zones', views.BusZones.as_view(), name="bus_zones")
]

urlpatterns = format_suffix_patterns(urlpatterns)
