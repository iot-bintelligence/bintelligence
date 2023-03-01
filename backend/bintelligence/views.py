from django.shortcuts import render
import requests
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import * 
from .serializers import *
import numpy as np
import tensorflow as tf


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

        print(request.data)
        return Response({"received data": request.data})

class PredictedValueView(views.APIView):

    # Load the saved model
    def __init__(self):
        self.model = tf.keras.models.load_model('../../ai/models/waste_model.h5')

    def get(self, request):
        last_measure = Measurement.objects.all().last()

        # Prepare the input data
        input_x = np.array([[last_measure.timestamp, last_measure.distance]])

        # Predict the timestamp when the container will be full
        predicted_full_timestamp = self.model.predict(input_x)[0][0]

        return Response({"last measurement": predicted_full_timestamp})