"""Factories for the review app."""
import factory

from django_libs.tests.factories import HvadFactoryMixin, UserFactory

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


class RatingCategoryFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``RatingCategory`` model."""
    FACTORY_FOR = models.RatingCategory

    language_code = 'en'
    name = factory.Sequence(lambda x: 'Rating category {}'.format(x))


class RatingCategoryChoiceFactory(HvadFactoryMixin,
                                  factory.DjangoModelFactory):
    """Factory for the ``RatingCategoryChoice`` model."""
    FACTORY_FOR = models.RatingCategoryChoice

    ratingcategory = factory.SubFactory(RatingCategoryFactory)
    label = factory.Sequence(lambda n: 'label {0}'.format(n))
    value = factory.Sequence(lambda n: str(n))


class RatingFactory(factory.DjangoModelFactory):
    """Factory for the ``Rating`` model."""
    FACTORY_FOR = models.Rating

    value = '3'
    review = factory.SubFactory(ReviewFactory)
    category = factory.SubFactory(RatingCategoryFactory)
