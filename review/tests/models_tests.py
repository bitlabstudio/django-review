"""Tests for the models of the review app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .factories import ReviewFactory, ReviewExtraInfoFactory


class ReviewTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.review = ReviewFactory()

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


class ReviewExtraInfoTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.extra_info = ReviewExtraInfoFactory()

    def test_instance(self):
        self.assertTrue(self.extra_info.pk, msg=(
            'Review extra info model should have been created.'))
