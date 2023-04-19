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
from datetime import datetime, timedelta


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

        use_model = False

        latest_measurement = Measurement.objects.latest()

        last_10 = Measurement.objects.all().order_by('-timestamp')[:10]

        # Make a list of the last 10 measurements
        measurement_list = []
        for measurement in last_10:
            measurement_list.append(measurement.distance)

        if use_model:
            # Make a prediction
            res = self.forecast(measurement_list)
        else:
            date, hours, minutes, percent = self.predict_dummy_data(latest_measurement.timestamp, latest_measurement.distance)
            
            # convert to desired format
            date = date.strftime("%Y-%m-%d %H:%M:%S")

            # If hours is greater than 24, calculate the number of days
            if hours > 24:
                # Convert hours into days
                hours = str(hours // 24) + " dager"
            else:
                # Convert hours into hours
                hours = str(hours) + " timer"

            res = {
                "date": date,
                "time": hours,
                "percent": str(percent) + "%",
                "measurement": latest_measurement.distance
            }
        
        return Response(res)
    
    def forecast(self, distance):
        df = pd.DataFrame({'measurement': [distance]})
        X, _, _ = self.df_to_x_y(df, window_size=0)
        pred = self.model.predict(X)
        return pred
    
    def df_to_x_y(self, df, window_size):
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

    def predict_dummy_data(self, timestamp, distance):
        # Return a timestamp for when the measure is full based on the current distance
        # and the timestamp of the last measurement

        original_timestamp = datetime.fromisoformat(str(timestamp))
        # add 1 hour and 30 minutes
        if distance > 220:
            return original_timestamp + timedelta(hours=62, minutes=30), 62, 30, 3
        elif distance > 200:
            return original_timestamp + timedelta(hours=50), 50, 0, 10
        elif distance > 180:
            return original_timestamp + timedelta(hours=40, minutes=30), 40, 30, 23
        elif distance > 160:
            return original_timestamp + timedelta(hours=30), 30, 0, 32
        elif distance > 140:
            return original_timestamp + timedelta(hours=20, minutes=30), 20, 30, 45
        elif distance > 120:
            return original_timestamp + timedelta(hours=10), 10, 0, 56
        elif distance > 100:
            return original_timestamp + timedelta(hours=5, minutes=30), 5, 30, 67
        elif distance > 80:
            return original_timestamp + timedelta(hours=2), 2, 0, 78
        elif distance > 60:
            return original_timestamp + timedelta(minutes=30), 0, 30, 89
        else:
            return original_timestamp + timedelta(minutes=15), 0, 15, 99
    
