"""Test for the template tags of the ``review`` app."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from mixer.backend.django import mixer

from ..templatetags import review_tags
from .test_app.models import WeatherCondition


class GetReviewsTestCase(TestCase):
    """Tests for the ``get_reviews`` template tag."""
    longMessage = True

    def setUp(self):
        self.reviewed_item = mixer.blend('test_app.WeatherCondition')
        self.review = mixer.blend(
            'review.Review',
            content_type=ContentType.objects.get_for_model(WeatherCondition),
            reviewed_item=self.reviewed_item)

    def test_tag(self):
        self.assertEqual(len(review_tags.get_reviews(self.reviewed_item)), 1)
        self.review.delete()
        self.assertEqual(len(review_tags.get_reviews(self.reviewed_item)), 0)


class GetReviewAverageTestCase(TestCase):
    """Tests for the ``get_review_average`` template tag."""
    longMessage = True

    def setUp(self):
        self.reviewed_item = mixer.blend('test_app.WeatherCondition')

    def test_tag(self):
        self.assertFalse(review_tags.get_review_average(self.reviewed_item))
        review = mixer.blend(
            'review.Review', reviewed_item=self.reviewed_item,
            content_type=ContentType.objects.get_for_model(WeatherCondition),
            object_id=self.reviewed_item.pk,
        )
        self.assertEqual(review_tags.get_review_average(self.reviewed_item), 0)
        rating = mixer.blend('review.Rating', review=review)
        mixer.blend('review.Rating', review=review, category=rating.category)
        """
        Fix those tests!
        self.assertEqual(review_tags.get_review_average(self.reviewed_item), 3)

        """


class GetReviewCountTestCase(TestCase):
    """Tests for the ``get_review_count`` template tag."""
    longMessage = True

    def setUp(self):
        self.reviewed_item = mixer.blend('test_app.WeatherCondition')
        self.review = mixer.blend(
            'review.Review',
            content_type=ContentType.objects.get_for_model(WeatherCondition),
            reviewed_item=self.reviewed_item)

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
        self.reviewed_item = mixer.blend('test_app.WeatherCondition')
        self.review = mixer.blend(
            'review.Review',
            content_type=ContentType.objects.get_for_model(WeatherCondition),
            reviewed_item=self.reviewed_item)

    def test_tag(self):
        expected_value = {
            'reviewed_item': self.reviewed_item,
            'category_averages': {},
        }
        self.assertEqual(
            review_tags.render_category_averages(self.reviewed_item, 5),
            expected_value)

        self.rating = mixer.blend(
            'review.Rating', review=self.review, value='2')
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
        self.review = mixer.blend(
            'review.Review', reviewed_item=self.reviewed_item,
            object_id=self.reviewed_item.pk,
            content_type=ContentType.objects.get_for_model(WeatherCondition))
        # the test_tag case was merely to cover some basic functionality. This
        # goes more in depth.
        rating1 = mixer.blend('review.Rating', review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 5):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=rating1.category, value=i)
        rating2 = mixer.blend('review.Rating', review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 7):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=rating2.category, value=i)
        mixer.blend('review.Rating', category=rating2.category,
                    review=self.review, value=None)
        mixer.blend('review.Rating', category=rating2.category,
                    review=self.review, value=None)

        """
        Fix those tests!
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

        """


class TotalReviewAverageTestCase(TestCase):
    """Tests for the ``total_review_average`` template tag."""
    longMessage = True

    def setUp(self):
        self.content_object = mixer.blend('test_app.WeatherCondition')
        self.review = mixer.blend(
            'review.Review', reviewed_item=self.content_object,
            content_type=ContentType.objects.get_for_model(WeatherCondition),
        )
        self.rating1 = mixer.blend('review.Rating', review=self.review,
                                   value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 5):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=self.rating1.category, value=i)
        self.rating2 = mixer.blend('review.Rating', review=self.review,
                                   value='6')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 7):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=self.rating2.category, value=i)

    def test_tag(self):
        self.assertEqual(
            review_tags.total_review_average(self.content_object), 100)
        mixer.blend('review.Rating', category=self.rating1.category,
                    review=self.review, value='0')
        mixer.blend('review.Rating', category=self.rating2.category,
                    review=self.review, value='0')
        self.assertEqual(
            review_tags.total_review_average(self.content_object), 50)
        mixer.blend('review.Rating', category=self.rating1.category,
                    review=self.review, value='')
        mixer.blend('review.Rating', category=self.rating2.category,
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
        self.user = mixer.blend('auth.User')
        self.content_object = mixer.blend('test_app.WeatherCondition')
        self.review = mixer.blend(
            'review.Review', user=self.user, reviewed_item=self.content_object,
            content_type=ContentType.objects.get_for_model(WeatherCondition),
        )
        self.other_user = mixer.blend('auth.User')

    def test_tag(self):
        self.assertTrue(
            review_tags.user_has_reviewed(self.content_object, self.user))
        self.assertFalse(
            review_tags.user_has_reviewed(self.content_object,
                                          self.other_user))
