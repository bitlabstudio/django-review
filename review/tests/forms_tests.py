"""Form tests for the ``review`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .factories import VotingCategoryFactory
from ..forms import ReviewForm
from ..models import Review, Voting


class ReviewFormTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()
        self.voting_category = VotingCategoryFactory()

    def test_form(self):
        form = ReviewForm(reviewed_item=self.content_object)
        self.assertTrue(form, msg=('Form has been initiated.'))

        data = {'category_{}'.format(self.voting_category.pk): '3'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 1, msg=(
            'One review should have been created.'))
        self.assertEqual(Voting.objects.count(), 1, msg=(
            'One voting should\'ve been created.'))
        self.assertEqual(
            Voting.objects.all()[0].review,
            Review.objects.all()[0],
            msg=('The voting\'s review should be equal the form\'s instance.'))
        self.assertEqual(
            Voting.objects.all()[0].category.pk,
            self.voting_category.pk,
            msg=('The voting\'s category should be saved.'))
        self.assertEqual(Voting.objects.all()[0].vote, '3', msg=(
            'The voting\'s value should be saved.'))
        self.assertIsNone(review.user, msg=('User should be None.'))

        form = ReviewForm(user=self.user, reviewed_item=self.content_object,
                          data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 2, msg=(
            'Another review should have been created.'))
        self.assertIsNotNone(review.user, msg=('User should be existant.'))
