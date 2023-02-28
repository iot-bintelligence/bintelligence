from django.db import models
from django.utils import timezone



class Device(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    firmware_version = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated_at']

        def __str__(self):
            return self.name


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']

        def __str__(self):
            return f'Temperature: {self.temperature}, Humidity: {self.humidity}'
