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


class VotingCategoryFactory(SimpleTranslationMixin, factory.Factory):
    """Factory for the ``VotingCategory`` model."""
    FACTORY_FOR = models.VotingCategory

    @staticmethod
    def _get_translation_factory_and_field():
        return (VotingCategoryTranslationFactory, 'category')


class VotingCategoryTranslationFactory(factory.Factory):
    """Factory for ``VotingCategoryTranslation`` objects."""
    FACTORY_FOR = models.VotingCategoryTranslation

    name = 'Voting category'
    category = factory.SubFactory(VotingCategoryFactory)
    language = 'en'


class VotingFactory(factory.DjangoModelFactory):
    """Factory for the ``Voting`` model."""
    FACTORY_FOR = models.Voting

    vote = '3'
    review = factory.SubFactory(ReviewFactory)
    category = factory.SubFactory(VotingCategoryFactory)
