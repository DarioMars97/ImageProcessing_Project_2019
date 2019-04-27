from rest_framework import serializers
from .models import Bus, Zone, Image


# class BusNoSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     bus_number = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return BusNo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.bus_number = validated_data.get('bus_number', instance.bus_number)
#         instance.save()
#         return instance


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'zone_text')


class BusSerializer(serializers.ModelSerializer):
    zones = ZoneSerializer(required=False, read_only=False, many=True)

    class Meta:
        model = Bus
        fields = ('id', 'bus_number', 'zones', 'link')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'text')
