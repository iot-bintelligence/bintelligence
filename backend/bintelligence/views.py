from django.shortcuts import render
import requests
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import * 
from .serializers import *
import base64

def my_view(request):
    response = requests.get('https://api.agify.io/?name=meelad')
    ip = response.json()
    context = {
        'title': 'My Page',
        'ip': ip,
    }
    return render(request, 'my_template.html', context)

class DeviceList(generics.ListCreateAPIView):
        queryset = Device.objects.all()
        serializer_class = DeviceSerializer
        http_method_names = ['get', 'post']

class MeasurementList(generics.ListCreateAPIView):
        queryset = Measurement.objects.all()
        serializer_class = MeasurementSerializer
        http_method_names = ['get']

class TestList(views.APIView):
    def get(self, request): 
        data = [{"name":"ivan"},{"name":"erik"}]
        serializer_class = TestSerializer(data, many=True).data
        return Response(serializer_class)

class SpanInput(views.APIView):
    def post(self, request):
        parser_classes = [JSONParser]
        
        # to do
        #create object in db from request's payload
        data = request.data["messages"]
        payload = data[0]["payload"]
        distance_hex = base64.b64decode(payload)
        distance_int = int.from_bytes(distance_hex,"big")

        #TODO change to find device by ID

        device = Device.objects.all().last()        
        measurement = Measurement(device = device, distance = distance_int, temperature = 0, humidity = 0)
        measurement.save()

        print(distance_int)

        #return Response({"received data": request.data})
        return Response({"Distance mm" : distance_int})

class PredictedValueView(views.APIView):
    def get(self, request):
        last_measure = Measurement.objects.all().last()
        
        #use model to predict output

        return Response({"last measurement": last_measurement})
