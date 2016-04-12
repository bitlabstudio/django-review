"""Tests for the models of the review app."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.timezone import now, timedelta

from mixer.backend.django import mixer

from .test_app.models import WeatherCondition


class ReviewTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.review = mixer.blend(
            'review.Review', content_type=ContentType.objects.get_for_model(
                WeatherCondition))

    def test_instance(self):
        self.assertTrue(self.review.pk, msg=(
            'Review model should have been created.'))

    def test_get_user(self):
        self.assertEqual(self.review.get_user(), 'Anonymous', msg=(
            'Should return anonymous.'))
        self.user = mixer.blend('auth.User')
        self.review.user = self.user
        self.assertEqual(self.review.get_user(), self.user.email, msg=(
            'Should return a user\'s email.'))

    def test_get_average_rating(self):
        self.assertFalse(self.review.get_average_rating(), msg=(
            'If there are no ratings, it should return False.'))
        mixer.blend('review.Rating', review=self.review, value='2')
        mixer.blend('review.Rating', review=self.review, value='4')
        self.assertEqual(self.review.get_average_rating(), 3, msg=(
            'Should return the average rating value.'))

        mixer.blend('review.Rating', review=self.review, value='')
        mixer.blend('review.Rating', category__counts_for_average=False,
                    review=self.review, value=0.0)
        self.assertEqual(self.review.get_average_rating(), 3, msg=(
            'Should return the average rating value and exclude the nullified'
            ' ones.'))

    def test_get_average_rating_with_custom_choices(self):
        self.assertFalse(self.review.get_average_rating(), msg=(
            'If there are no ratings, it should return False.'))
        rating1 = mixer.blend('review.Rating', review=self.review, value='4')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 5):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=rating1.category, value=i)
        rating2 = mixer.blend('review.Rating', review=self.review, value='6')
        # we create choices to simulate, that the previous value was the max
        for i in range(0, 7):
            mixer.blend('review.RatingCategoryChoiceTranslation',
                        language_code='en-us',
                        ratingcategory=rating2.category, value=i)
        mixer.blend('review.Rating', category=rating2.category,
                    review=self.review, value='6')
        mixer.blend('review.Rating', category=rating2.category,
                    review=self.review, value=None)
        # testing the absolute max voting
        self.assertEqual(self.review.get_average_rating(6), 6, msg=(
            'Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(4), 4, msg=(
            'Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(100), 100, msg=(
            'Should return the average rating value.'))

        # testing the category averages
        """
        Fix those tests!

        self.assertEqual(
            self.review.get_category_averages(6),
            {rating1.category: 6.0, rating2.category: 6.0},
            msg=('Should return the average ratings for the category.'))

        self.assertEqual(
            self.review.get_category_averages(),
            {rating1.category: 6.0, rating2.category: 6.0},
            msg=('Should return the average ratings for the category.'))

        self.assertEqual(
            self.review.get_category_averages(100),
            {rating1.category: 100.0, rating2.category: 100.0},
            msg=('Should return the average ratings for the category.'))

        # these ratings should not change results and should just be ignored
        mixer.blend('review.Rating', category=rating2.category,
                    review=self.review, value='')
        mixer.blend('review.Rating', review=self.review, value='')
        self.assertEqual(self.review.get_average_rating(6), 6, msg=(
            'Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(4), 4, msg=(
            'Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(100), 100, msg=(
            'Should return the average rating value.'))

        # altering the ratings to get a very low voting
        rating1.value = '1'
        rating1.save()
        rating2.value = '1'
        rating2.save()
        rating3.value = '1'
        rating3.save()
        self.assertEqual(self.review.get_average_rating(6), 1.25,
                         msg=('Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(4), 0.8333333333333333,
                         msg=('Should return the average rating value.'))
        self.assertEqual(
            self.review.get_average_rating(100),
            20.833333333333336, msg=(
                'Should return the average rating value.'))

        # and finally the lowest possible voting
        rating1.value = '0'
        rating1.save()
        rating2.value = '0'
        rating2.save()
        rating3.value = '0'
        rating3.save()
        self.assertEqual(self.review.get_average_rating(6), 0,
                         msg=('Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(4), 0,
                         msg=('Should return the average rating value.'))
        self.assertEqual(self.review.get_average_rating(100), 0,
                         msg=('Should return the average rating value.'))

        """

    def test_is_editable(self):
        self.assertTrue(self.review.is_editable(), msg=(
            'Should be editable, if period setting is not set.'))
        with self.settings(REVIEW_UPDATE_PERIOD=1):
            self.assertTrue(self.review.is_editable(), msg=(
                'Should be editable, if period has not ended yet.'))
            self.review.creation_date = now() - timedelta(days=1)
            self.review.save()
            self.assertFalse(self.review.is_editable(), msg=(
                'Should return False, if period has ended.'))


class ReviewExtraInfoTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.extra_info = mixer.blend(
            'review.ReviewExtraInfo',
            review=mixer.blend('review.Review',
                               content_type=ContentType.objects.get_for_model(
                                   WeatherCondition)),
            content_type=ContentType.objects.get_for_model(WeatherCondition))

    def test_instance(self):
        self.assertTrue(self.extra_info.pk, msg=(
            'Review extra info model should have been created.'))


class RatingCategoryTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.category = mixer.blend('review.RatingCategoryTranslation',
                                    language_code='en-us')

    def test_instance(self):
        self.assertTrue(self.category.pk, msg=(
            'Rating category model should have been created.'))


class RatingCategoryChoiceTestCase(TestCase):
    """Tests for the ``RatingCategoryChoice`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``RatingCategoryChoice`` model."""
        ratingcategorychoice = mixer.blend(
            'review.RatingCategoryChoiceTranslation', language_code='en-us')
        self.assertTrue(ratingcategorychoice.pk)


class RatingTestCase(TestCase):
    longMessage = True

    def setUp(self):
        review = mixer.blend(
            'review.Review', content_type=ContentType.objects.get_for_model(
                WeatherCondition))
        self.rating = mixer.blend('review.Rating', review=review)

    def test_instance(self):
        self.assertTrue(self.rating.pk, msg=(
            'Rating model should have been created.'))
