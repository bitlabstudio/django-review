"""Factories for the review app."""
import factory

from django_libs.tests.factories import UserFactory
from django_libs.tests.factories import SimpleTranslationMixin

from .. import models


class ReviewFactory(factory.DjangoModelFactory):
    """Factory for the ``Review`` model."""
    FACTORY_FOR = models.Review

    reviewed_item = factory.SubFactory(UserFactory)


class ReviewExtraInfoFactory(factory.DjangoModelFactory):
    """Factory for the ``ReviewExtraInfo`` model."""
    FACTORY_FOR = models.ReviewExtraInfo

    review = factory.SubFactory(ReviewFactory)
    type = 'extra_information'
    content_object = factory.SubFactory(UserFactory)


class RatingCategoryFactory(SimpleTranslationMixin,
                            factory.DjangoModelFactory):
    """Factory for the ``RatingCategory`` model."""
    FACTORY_FOR = models.RatingCategory

    @staticmethod
    def _get_translation_factory_and_field():
        return (RatingCategoryTranslationFactory, 'category')


class RatingCategoryTranslationFactory(factory.DjangoModelFactory):
    """Factory for ``RatingCategoryTranslation`` objects."""
    FACTORY_FOR = models.RatingCategoryTranslation

    name = 'Rating category'
    category = factory.SubFactory(RatingCategoryFactory)
    language = 'en'


class RatingFactory(factory.DjangoModelFactory):
    """Factory for the ``Rating`` model."""
    FACTORY_FOR = models.Rating

    value = '3'
    review = factory.SubFactory(ReviewFactory)
    category = factory.SubFactory(RatingCategoryFactory)
