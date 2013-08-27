"""Tests for the models of the review app."""
from django.test import TestCase

from .factories import ReviewFactory, ReviewExtraInfoFactory


class ReviewTestCase(TestCase):
    def setUp(self):
        self.review = ReviewFactory()

    def test_instance(self):
        self.assertTrue(self.review.pk, msg=(
            'Review model should have been created.'))


class ReviewExtraInfoTestCase(TestCase):
    def setUp(self):
        self.extra_info = ReviewExtraInfoFactory()

    def test_instance(self):
        self.assertTrue(self.extra_info.pk, msg=(
            'Review extra info model should have been created.'))
