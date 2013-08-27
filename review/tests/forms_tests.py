"""Form tests for the ``review`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..forms import ReviewForm
from ..models import Review


class ReviewFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()

    def test_form(self):
        form = ReviewForm(reviewed_item=self.content_object)
        self.assertTrue(form, msg=('Form has been initiated.'))

        data = {}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 1, msg=(
            'One review should have been created.'))
        self.assertIsNone(review.user, msg=('User should be None.'))

        form = ReviewForm(user=self.user, reviewed_item=self.content_object,
                          data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 2, msg=(
            'Another review should have been created.'))
        self.assertIsNotNone(review.user, msg=('User should be existant.'))
