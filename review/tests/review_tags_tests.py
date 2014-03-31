"""Test for the template tags of the ``review`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..templatetags.review_tags import total_review_average, user_has_reviewed
from . import factories


class TotalReviewAverageTestCase(TestCase):
    """Tests for the ``total_review_average`` template tag."""
    longMessage = True

    def setUp(self):
        self.content_object = UserFactory()
        self.review = factories.ReviewFactory(
            reviewed_item=self.content_object)
        self.rating1 = factories.RatingFactory(review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 5):
            factories.RatingCategoryChoiceFactory(
                ratingcategory=self.rating1.category, value=i)
        self.rating2 = factories.RatingFactory(review=self.review, value='6')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 7):
            factories.RatingCategoryChoiceFactory(
                ratingcategory=self.rating2.category, value=i)

    def test_tag(self):
        self.assertEqual(total_review_average(self.content_object), 100)
        factories.RatingFactory(
            category=self.rating1.category,
            review=self.review, value='0')
        factories.RatingFactory(
            category=self.rating2.category,
            review=self.review, value='0')
        self.assertEqual(total_review_average(self.content_object), 50)
        factories.RatingFactory(
            category=self.rating1.category,
            review=self.review, value=None)
        factories.RatingFactory(
            category=self.rating2.category,
            review=self.review, value=None)
        self.assertEqual(total_review_average(self.content_object), 50)
        self.assertEqual(total_review_average(self.content_object, 10), 5)
        self.assertEqual(total_review_average(self.content_object, 5), 2.5)


class UserHasReviewedTestCase(TestCase):
    """Tests for the ``user_has_reviewed`` template tag."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()
        self.review = factories.ReviewFactory(
            user=self.user,
            reviewed_item=self.content_object)
        self.other_user = UserFactory()

    def test_tag(self):
        self.assertTrue(user_has_reviewed(self.content_object, self.user))
        self.assertFalse(user_has_reviewed(self.content_object,
                                           self.other_user))
