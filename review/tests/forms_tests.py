"""Form tests for the ``review`` app."""
from django.test import TestCase

from mixer.backend.django import mixer

from ..forms import ReviewForm
from ..models import Review, Rating


class ReviewFormTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.content_object = mixer.blend('auth.User')
        self.rating_category = mixer.blend('review.RatingCategoryTranslation',
                                           language_code='en-us').master

    def test_form(self):
        form = ReviewForm(reviewed_item=self.content_object)
        self.assertTrue(form, msg=('Form has been initiated.'))

        with self.settings(
                REVIEW_FORM_CHOICE_WIDGET='django.forms.RadioSelect'):
            form = ReviewForm(reviewed_item=self.content_object)
            self.assertTrue(form, msg=('Form has been initiated.'))

        data = {'category_{0}'.format(self.rating_category.pk): '3'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))

        review = form.save()
        self.assertEqual(Review.objects.count(), 1, msg=(
            'One review should have been created.'))
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

        self.new_category = mixer.blend('review.RatingCategoryTranslation',
                                        language_code='en-us')
        form = ReviewForm(instance=review, reviewed_item=self.content_object)
        self.assertEqual(
            form.initial.get('category_{0}'.format(self.rating_category.pk)),
            '3', msg=('The form\'s initial should contain the ratings.'))
        self.assertFalse(
            form.initial.get('category_{0}'.format(self.new_category.pk)),
            msg=('The form\'s initial should not contain a new category.'))

    def test_form_with_custom_choices(self):
        # Create custom choices
        choices = []
        expected_choices = []
        for j in range(1, 4):
            i = 5 - j
            choices.append(mixer.blend(
                'review.RatingCategoryChoiceTranslation',
                language_code='en-us', ratingcategory=self.rating_category,
                value=i, label=str(i)).master)
            expected_choices.append((u'{}'.format(i), u'{}'.format(i)))

        """
        Disabled.
        Find a way to let hvad work with mixer.

        form = ReviewForm(reviewed_item=self.content_object)
        self.assertTrue(form, msg=('Form has been initiated.'))
        field_name = 'category_{0}'.format(self.rating_category.pk)
        self.assertTrue(form[field_name], msg='The field was added')
        self.assertEqual(form[field_name].field.choices, expected_choices,
                         msg=('The field choices were not added correctly from'
                              ' the RatingCategegoryChoice instances.'))

        data = {'category_{0}'.format(self.rating_category.pk): '5'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertFalse(form.is_valid(), msg=(
            'When assigning a higher value, than there are'
            ' RatingCategoryChoice objects, the form should not be valid.'))

        data = {'category_{0}'.format(self.rating_category.pk): '3'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'Even when answering without value and nullifying the category,'
            ' the form should be valid. Errors: {0}'.format(form.errors)))

        data = {'category_{0}'.format(self.rating_category.pk): '3'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        review = form.save()
        self.assertEqual(Review.objects.count(), 1, msg=(
            'One review should have been created.'))
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

        mixer.blend('review.RatingCategoryChoiceTranslation',
                    language_code='en-us', ratingcategory=self.rating_category,
                    value=0, label='0')
        data = {'content': 'foo',
                'category_{0}'.format(self.rating_category.pk): None}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertFalse(form.is_valid(), msg=(
            'You should not be able to rate a category with None if there'
            ' is no None choice.'))

        data = {'content': 'foobar'}
        form = ReviewForm(reviewed_item=self.content_object, data=data)
        self.assertFalse(form.is_valid(), msg=(
            'Without any choice selected, the form should be invalid.'))

        """
