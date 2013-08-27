"""Factories for the review app."""
import factory

from django_libs.tests.factories import UserFactory

from ..models import Review


class ReviewFactory(factory.DjangoModelFactory):
    """Factory for the ``Review`` model."""
    FACTORY_FOR = Review

    reviewed_item = factory.SubFactory(UserFactory)
