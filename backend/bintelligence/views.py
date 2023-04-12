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
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv


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
        model_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'model.h5')
        self.model = tf.keras.models.load_model(model_path)

    def get(self, request):
        
        # TODO predict the value
        """
        measurements = Measurement.objects.all().values()
        measurement_list = list(measurements)

        # COnvert the timestamp to datetime
        for measurement in measurement_list:
            measurement["timestamp"] = pd.to_datetime(measurement["timestamp"], format='%Y-%m-%d %H:%M:%S')

        # self.create_csv(measurement_list)
        """

        latest_measurement = Measurement.objects.latest('timestamp')

        print(latest_measurement)

        measurement = self.predict_measurement(request, latest_measurement)
        
        return Response({"predicted_value": measurement})
    
    def predict_measurement(self, request, data):
        # Convert the input data to a numpy array
        data = np.array(data.split(','), dtype=float)

        # Prepare the input data
        window_size = 24
        X, y, timestamps = self.df_to_x_y(data, window_size)
        latest_data_point = np.array(X[-1])

        # Make a prediction
        prediction = self.model.predict(latest_data_point)

        # Return the predicted value as a JSON response
        return prediction
    
    def df_to_x_y(self, df, window_size=5):
        df_as_numpy = df.to_numpy()
        timestamps = df.index[window_size:]
        X = []
        y = []
        for i in range(len(df_as_numpy) - window_size):
            row = [[x] for x in df_as_numpy[i:i + window_size]]
            X.append(row)
            label = df_as_numpy[i + window_size]
            y.append(label)
        return np.array(X), np.array(y), timestamps
    
    def create_csv(self, measurement_list):
        with open('data.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=measurement_list[0].keys())
            writer.writeheader()
            for d in measurement_list:
                writer.writerow(d)
    
