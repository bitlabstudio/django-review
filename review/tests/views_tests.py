"""View tests for the ``review`` app."""
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import views
from ..models import Review
from .test_app.models import WeatherCondition


class ReviewCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = views.ReviewCreateView

    def setUp(self):
        self.content_object = mixer.blend('auth.User')
        self.user = mixer.blend('auth.User', first_name='')

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

        self.is_callable(user=self.user, msg=(
            'View should be callable by an authenticated user.'))

        with self.settings(REVIEW_AVOID_MULTIPLE_REVIEWS=True):
            def has_perm(u, item):
                return self.user_has_perm(u)
            with self.settings(REVIEW_PERMISSION_FUNCTION=has_perm):
                self.is_not_callable(post=True, user=self.user, msg=(
                    'View should not be callable due to missing permissions.'))
                self.assertEqual(Review.objects.count(), 0, msg=(
                    'No reviews should\'ve been created.'))
                self.user.first_name = 'Foo'
                self.user.save()
                self.is_postable(
                    user=self.user, to_url_name='review_detail', msg=(
                        'View should be callable by an authenticated user.'))
                self.assertEqual(Review.objects.count(), 1, msg=(
                    'One review should\'ve been created.'))
            self.is_postable(
                to=reverse('review_update', kwargs={
                    'pk': Review.objects.all()[0].pk}),
                user=self.user, msg=(
                    'View should redirect, if review alreasy exists.'))
            self.assertEqual(Review.objects.count(), 1, msg=(
                'No new review should\'ve been created.'))

        with self.settings(REVIEW_CUSTOM_FORM='test_app.FooReviewForm'):
            self.is_callable(user=self.user)

        with self.settings(REVIEW_CUSTOM_FORM='foo.BarForm'):
            self.is_callable(user=self.user)

        with self.settings(
                REVIEW_CUSTOM_FORM='test_app.forms.CustomReviewForm'):
            data = {
                'weather_conditions': mixer.blend(
                    'test_app.WeatherCondition').pk,
            }
            self.is_postable(data=data, user=self.user,
                             to_url_name='review_detail')

        with self.settings(REVIEW_UPDATE_SUCCESS_URL='review_list'):
            self.is_postable(data=data, user=self.user,
                             to=reverse('review_list'))

        with self.settings(REVIEW_ALLOW_ANONYMOUS=True):
            self.is_callable(msg=(
                'View should be callable as an anonymous user.'))


class ReviewDetailViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = views.ReviewDetailView

    def setUp(self):
        self.review = mixer.blend(
            'review.Review',
            object_id=mixer.blend('test_app.WeatherCondition').pk,
            content_type=ContentType.objects.get_for_model(WeatherCondition))

    def get_view_name(self):
        return 'review_detail'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_callable()


class ReviewUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = views.ReviewUpdateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.other_user = mixer.blend('auth.User')
        self.review = mixer.blend(
            'review.Review', user=self.user,
            object_id=mixer.blend('test_app.WeatherCondition').pk,
            content_type=ContentType.objects.get_for_model(WeatherCondition))

    def get_view_name(self):
        return 'review_update'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_not_callable(user=self.other_user)
        self.is_callable(user=self.user)

        with self.settings(REVIEW_UPDATE_PERIOD=1):
            self.is_callable(user=self.user, msg=(
                'Should be callable, if period hasn\'t ended yet.'))
            self.review.creation_date = timezone.now() - timezone.timedelta(
                seconds=120)
            self.review.save()
            self.redirects(
                to=reverse('review_detail', kwargs={'pk': self.review.pk}),
                user=self.user, msg=('Should redirect, if period has ended.'))


class ReviewDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = views.ReviewDeleteView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.review = mixer.blend(
            'review.Review', user=self.user,
            object_id=mixer.blend('test_app.WeatherCondition').pk,
            content_type=ContentType.objects.get_for_model(WeatherCondition))

    def get_view_name(self):
        return 'review_delete'

    def get_view_kwargs(self):
        return {'pk': self.review.pk}

    def test_view(self):
        self.is_postable(user=self.user, to='/')
        self.review = mixer.blend(
            'review.Review', user=self.user,
            object_id=mixer.blend('test_app.WeatherCondition').pk,
            content_type=ContentType.objects.get_for_model(WeatherCondition))
        with self.settings(REVIEW_DELETION_SUCCESS_URL='review_list'):
            self.is_postable(user=self.user, to_url_name='review_list')
