
from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 30)

    class Meta:
        model = Device
        fields = '__all__'
