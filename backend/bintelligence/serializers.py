
from rest_framework import serializers
from .models import *

class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 30)

    class Meta:
        model = Device
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField()
    distance = serializers.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        model = Measurement
        fields = '__all__'




class TestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 30)
