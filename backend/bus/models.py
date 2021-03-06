from django.db import models


class Zone(models.Model):
    zone_text = models.CharField(max_length=60, unique=True)


class Bus(models.Model):
    bus_number = models.IntegerField(unique=True)
    zones = models.ManyToManyField(Zone)
    link = models.TextField(null=True)


def bus_file(_, filename):
    return '/'.join(['buses', filename])


class Image(models.Model):
    image = models.ImageField(
        upload_to=bus_file,
        max_length=254, blank=True, null=True
    )
    text = models.TextField(null=True)
