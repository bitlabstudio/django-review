"""Tests for the models of the review app."""
from django.test import TestCase

from .factories import ReviewFactory


class ReviewTestCase(TestCase):
    def setUp(self):
        self.review = ReviewFactory()

    def test_instance(self):
        self.assertTrue(self.review.pk, msg=(
            'Review model should have been created.'))
