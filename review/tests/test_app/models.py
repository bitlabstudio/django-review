from django.db import models


class WeatherCondition(models.Model):
    name = models.CharField(max_length=20)
