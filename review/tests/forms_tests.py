"""Form tests for the ``review`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .factories import RatingCategoryFactory
from ..forms import ReviewForm
from ..models import Review, Rating


class ReviewFormTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()
        self.rating_category = RatingCategoryFactory()

    def test_form(self):
        form = ReviewForm(reviewed_item=self.content_object)
        self.assertTrue(form, msg=('Form has been initiated.'))

        data = {'category_{}'.format(self.rating_category.pk): '3'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 1, msg=(
            'One review should have been created.'))
        self.assertEqual(Rating.objects.count(), 1, msg=(
            'One rating should\'ve been created.'))
        self.assertEqual(
            Rating.objects.all()[0].review,
            Review.objects.all()[0],
            msg=('The rating\'s review should be equal the form\'s instance.'))
        self.assertEqual(
            Rating.objects.all()[0].category.pk,
            self.rating_category.pk,
            msg=('The rating\'s category should be saved.'))
        self.assertEqual(Rating.objects.all()[0].value, '3', msg=(
            'The rating\'s value should be saved.'))
        self.assertIsNone(review.user, msg=('User should be None.'))

        form = ReviewForm(user=self.user, reviewed_item=self.content_object,
                          data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 2, msg=(
            'Another review should have been created.'))
        self.assertIsNotNone(review.user, msg=('User should be existant.'))

        self.new_category = RatingCategoryFactory()
        form = ReviewForm(instance=review, reviewed_item=self.content_object)
        self.assertEqual(
            form.initial.get('category_{}'.format(self.rating_category.pk)),
            '3', msg=('The form\'s initial should contain the ratings.'))
        self.assertFalse(
            form.initial.get('category_{}'.format(self.new_category.pk)),
            msg=('The form\'s initial should not contain a new category.'))
