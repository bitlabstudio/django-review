"""Tests for the models of the review app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from . import factories


class ReviewTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.review = factories.ReviewFactory()

    def test_instance(self):
        self.assertTrue(self.review.pk, msg=(
            'Review model should have been created.'))

    def test_get_user(self):
        self.assertEqual(self.review.get_user(), 'Anonymous', msg=(
            'Should return anonymous.'))
        self.user = UserFactory()
        self.review.user = self.user
        self.assertEqual(self.review.get_user(), self.user.email, msg=(
            'Should return a user\'s email.'))

    def test_get_average_voting(self):
        self.assertFalse(self.review.get_average_voting(), msg=(
            'If there are no votings, it should return False.'))
        factories.VotingFactory(review=self.review, vote='2')
        factories.VotingFactory(review=self.review, vote='4')
        self.assertEqual(self.review.get_average_voting(), 3, msg=(
            'Should return the average voting value.'))


class ReviewExtraInfoTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.extra_info = factories.ReviewExtraInfoFactory()

    def test_instance(self):
        self.assertTrue(self.extra_info.pk, msg=(
            'Review extra info model should have been created.'))


class VotingCategoryTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.category = factories.VotingCategoryFactory()

    def test_instance(self):
        self.assertTrue(self.category.pk, msg=(
            'Voting category model should have been created.'))


class VotingTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.voting = factories.VotingFactory()

    def test_instance(self):
        self.assertTrue(self.voting.pk, msg=(
            'Voting model should have been created.'))
