from django.urls import path


from . import views


urlpatterns = [
    path('', views.busView, name="bus_home")
]
