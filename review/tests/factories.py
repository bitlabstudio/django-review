"""Factories for the review app."""
import factory

from django_libs.tests.factories import UserFactory

from ..models import Review, ReviewExtraInfo


class ReviewFactory(factory.DjangoModelFactory):
    """Factory for the ``Review`` model."""
    FACTORY_FOR = Review

    reviewed_item = factory.SubFactory(UserFactory)


class ReviewExtraInfoFactory(factory.DjangoModelFactory):
    """Factory for the ``ReviewExtraInfo`` model."""
    FACTORY_FOR = ReviewExtraInfo

    review = factory.SubFactory(ReviewFactory)
    type = 'extra_information'
    content_object = factory.SubFactory(UserFactory)
