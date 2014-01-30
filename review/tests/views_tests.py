"""View tests for the ``review`` app."""
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from .factories import ReviewFactory
from ..models import Review, ReviewExtraInfo
from test_app.factories import WeatherConditionFactory


class ReviewCreateViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        self.content_object = UserFactory()
        self.user = UserFactory()

    def get_view_name(self):
        return 'review_create'

    def get_view_kwargs(self):
        return {
            'content_type': ContentType.objects.get_for_model(
                self.content_object),
            'object_id': self.content_object.pk,
        }

    def user_has_perm(self, user):
        # Simulates permission for the current user
        if user.first_name:
            return True
        return False

    def test_view(self):
        wrong_kwargs = {
            'content_type': 'Foo',
            'object_id': self.content_object.pk,
        }
        self.is_not_callable(kwargs=wrong_kwargs)

        wrong_kwargs = {
            'content_type': ContentType.objects.get_for_model(
                self.content_object),
            'object_id': '999',
        }
        self.is_not_callable(kwargs=wrong_kwargs)

        self.is_callable(user=self.user, message=(
            'View should be callable by an authenticated user.'))

        with self.settings(REVIEW_AVOID_MULTIPLE_REVIEWS=True):
            has_perm = lambda u, item: self.user_has_perm(u)
            with self.settings(REVIEW_PERMISSION_FUNCTION=has_perm):
                self.is_not_callable(method='post', user=self.user, message=(
                    'View should not be callable due to missing permissions.'))
                self.assertEqual(Review.objects.count(), 0, msg=(
                    'No reviews should\'ve been created.'))
                self.user.first_name = 'Foo'
                self.user.save()
                self.is_callable(method='post', user=self.user, message=(
                    'View should be callable by an authenticated user.'))
                self.assertEqual(Review.objects.count(), 1, msg=(
                    'One review should\'ve been created.'))
            self.is_callable(
                and_redirects_to=reverse('review_update', kwargs={
                    'pk': Review.objects.all()[0].pk}),
                method='post', user=self.user, message=(
                    'View should redirect, if review alreasy exists.'))
            self.assertEqual(Review.objects.count(), 1, msg=(
                'No new review should\'ve been created.'))

        with self.settings(REVIEW_CUSTOM_FORM='test_app.FooReviewForm'):
            self.is_callable()

        with self.settings(REVIEW_CUSTOM_FORM='foo.BarForm'):
            self.is_callable()

        with self.settings(
                REVIEW_CUSTOM_FORM='test_app.forms.CustomReviewForm'):
            data = {'weather_conditions': WeatherConditionFactory().pk}
            self.is_callable(method='post', data=data)
            self.assertEqual(ReviewExtraInfo.objects.count(), 1, msg=(
                'One review extra info should\'ve been created.'))

        with self.settings(REVIEW_UPDATE_SUCCESS_URL='review_list'):
            self.is_callable(method='post', data=data,
                             and_redirects_to=reverse('review_list'))

        with self.settings(REVIEW_ALLOW_ANONYMOUS=True):
            self.is_callable(anonymous=True, message=(
                'View should be callable as an anonymous user.'))


class ReviewDetailViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        self.review = ReviewFactory()

    def get_view_name(self):
        return 'review_detail'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_callable()


class ReviewUpdateViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.review = ReviewFactory(user=self.user)

    def get_view_name(self):
        return 'review_update'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_not_callable(user=self.other_user)
        self.is_callable(user=self.user)

        with self.settings(REVIEW_UPDATE_PERIOD=1):
            self.is_callable(message=(
                'Should be callable, if period hasn\'t ended yet.'))
            self.review.creation_date = timezone.now() - timezone.timedelta(
                seconds=120)
            self.review.save()
            self.is_callable(
                and_redirects_to=reverse('review_detail', kwargs={
                    'pk': self.review.pk}),
                message=('Should redirect, if period has ended.'))


class ReviewDeleteViewTestCase(ViewTestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.review = ReviewFactory(user=self.user)

    def get_view_name(self):
        return 'review_delete'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_callable(user=self.user, method='post')
        self.review = ReviewFactory(user=self.user)
        with self.settings(REVIEW_DELETION_SUCCESS_URL='review_list'):
            self.is_callable(user=self.user, method='post')
