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

    def test_get_average_rating(self):
        self.assertFalse(self.review.get_average_rating(), msg=(
            'If there are no ratings, it should return False.'))
        factories.RatingFactory(review=self.review, value='2')
        factories.RatingFactory(review=self.review, value='4')
        self.assertEqual(self.review.get_average_rating(), 3, msg=(
            'Should return the average rating value.'))


class ReviewExtraInfoTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.extra_info = factories.ReviewExtraInfoFactory()

    def test_instance(self):
        self.assertTrue(self.extra_info.pk, msg=(
            'Review extra info model should have been created.'))


class RatingCategoryTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.category = factories.RatingCategoryFactory()

    def test_instance(self):
        self.assertTrue(self.category.pk, msg=(
            'Rating category model should have been created.'))


class RatingTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.rating = factories.RatingFactory()

    def test_instance(self):
        self.assertTrue(self.rating.pk, msg=(
            'Rating model should have been created.'))
