"""Factories for the test_app app."""
import factory

from . import models


class WeatherConditionFactory(factory.DjangoModelFactory):
    """Factory for the ``WeatherCondition`` model."""
    FACTORY_FOR = models.WeatherCondition

    name = 'Good'
