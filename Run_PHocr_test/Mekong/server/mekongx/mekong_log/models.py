from django.db import models
from rest_framework import serializers


class MekongLog(models.Model):
    log_tag = models.CharField(max_length=255, blank=True)
    log_type = models.CharField(max_length=255, blank=True)
    at_time = models.DateTimeField("Logging time", blank=True)
    client_name = models.CharField(max_length=255, blank=True)
    client_address = models.CharField(max_length=255)
    message = models.CharField(max_length=4000, blank=True)


class MekongLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MekongLog
        fields = ('id', 'log_tag', 'log_type', 'at_time', 'client_name', 'client_address', 'message')
