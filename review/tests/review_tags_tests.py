"""Test for the template tags of the ``review`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..templatetags import review_tags
from . import factories


class GetReviewCountTestCase(TestCase):
    """Tests for the ``get_review_count`` template tag."""
    longMessage = True

    def setUp(self):
        self.reviewed_item = UserFactory()
        self.review = factories.ReviewFactory(reviewed_item=self.reviewed_item)

    def test_tag(self):
        self.assertEqual(
            review_tags.get_review_count(self.reviewed_item), 1)
        self.review.delete()
        self.assertEqual(
            review_tags.get_review_count(self.reviewed_item), 0)


class RenderCategoryAveragesTestCase(TestCase):
    """Tests for the ``render_category_averages`` template tag."""
    longMessage = True

    def setUp(self):
        self.reviewed_item = UserFactory()

    def test_tag(self):
        self.rating = factories.RatingFactory(
            review__reviewed_item=self.reviewed_item,
            value='2')
        expected_value = {
            'reviewed_item': self.reviewed_item,
            'category_averages': {self.rating.category: 2.0},
        }
        self.assertEqual(
            review_tags.render_category_averages(self.reviewed_item, 5),
            expected_value)

        expected_value = {
            'reviewed_item': self.reviewed_item,
            'category_averages': {self.rating.category: 40.0},
        }
        self.assertEqual(
            review_tags.render_category_averages(self.reviewed_item, 100),
            expected_value)

    def test_tag_more_extensively(self):
        self.review = factories.ReviewFactory(reviewed_item=self.reviewed_item)
        # the test_tag case was merely to cover some basic functionality. This
        # goes more in depth.
        rating1 = factories.RatingFactory(review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 5):
            factories.RatingCategoryChoiceFactory(
                ratingcategory=rating1.category, value=i)
        rating2 = factories.RatingFactory(review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 7):
            factories.RatingCategoryChoiceFactory(
                ratingcategory=rating2.category, value=i)
        factories.RatingFactory(
            category=rating2.category, review=self.review, value=None)
        factories.RatingFactory(
            category=rating2.category, review=self.review, value=None)

        expected_value = {
            'reviewed_item': self.reviewed_item,
            'category_averages': {
                rating1.category: 6.0,
                rating2.category: 4.0,
            },
        }

        self.assertEqual(
            review_tags.render_category_averages(self.reviewed_item, 6),
            expected_value,
        )


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
        self.assertEqual(
            review_tags.total_review_average(self.content_object), 100)
        factories.RatingFactory(
            category=self.rating1.category,
            review=self.review, value='0')
        factories.RatingFactory(
            category=self.rating2.category,
            review=self.review, value='0')
        self.assertEqual(
            review_tags.total_review_average(self.content_object), 50)
        factories.RatingFactory(
            category=self.rating1.category,
            review=self.review, value='')
        factories.RatingFactory(
            category=self.rating2.category,
            review=self.review, value='')
        self.assertEqual(
            review_tags.total_review_average(self.content_object), 50)
        self.assertEqual(
            review_tags.total_review_average(self.content_object, 10), 5)
        self.assertEqual(
            review_tags.total_review_average(self.content_object, 5), 2.5)


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
        self.assertTrue(
            review_tags.user_has_reviewed(self.content_object, self.user))
        self.assertFalse(
            review_tags.user_has_reviewed(self.content_object,
                                          self.other_user))
