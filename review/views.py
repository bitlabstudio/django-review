"""Views for the review app."""
import importlib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import ReviewForm
from .models import Review


#------ MIXINS ------#

class ReviewViewMixin(object):
    model = Review

    def dispatch(self, request, *args, **kwargs):
        # Check, if user needs to be logged in
        if getattr(settings, 'REVIEW_ALLOW_ANONYMOUS', False):
            return super(ReviewViewMixin, self).dispatch(
                request, *args, **kwargs)
        return login_required(super(ReviewViewMixin, self).dispatch)(
            request, *args, **kwargs)

    def get_form_class(self):
        if getattr(settings, 'REVIEW_CUSTOM_FORM', False):
            app_label, class_name = settings.REVIEW_CUSTOM_FORM.rsplit('.', 1)
            try:
                return getattr(importlib.import_module(app_label), class_name,
                               ReviewForm)
            except ImportError:
                pass
        return ReviewForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReviewViewMixin, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'reviewed_item': self.reviewed_item})
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        success_url = getattr(settings, 'REVIEW_UPDATE_SUCCESS_URL', None)
        if success_url is not None:
            if callable(success_url):
                return success_url(self.object)
            else:
                return reverse(success_url)
        return reverse('review_detail', kwargs={'pk': self.object.pk})


class ReviewUpdateMixin(object):
    """Mixin to provide update functions for a ``Review`` instance."""
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        if not self.object.user or self.object.user != request.user:
            raise Http404
        # Check, if update period is set and has ended
        if getattr(settings, 'REVIEW_UPDATE_PERIOD', False):
            period_end = self.object.creation_date + timezone.timedelta(
                seconds=getattr(settings, 'REVIEW_UPDATE_PERIOD') * 60)
            if timezone.now() > period_end:
                return HttpResponseRedirect(
                    reverse('review_detail', kwargs={'pk': self.object.pk}))
        self.reviewed_item = self.object.reviewed_item
        return super(ReviewUpdateMixin, self).dispatch(
            request, *args, **kwargs)


#------ MODEL VIEWS ------#

class ReviewCreateView(ReviewViewMixin, CreateView):
    """View to create a new ``Review`` instance."""
    def dispatch(self, request, *args, **kwargs):
        # Check, if content type exists
        try:
            self.content_type = ContentType.objects.get(
                model=kwargs.get('content_type'))
        except ContentType.DoesNotExist:
            raise Http404

        # Check, if reviewed item exists
        try:
            self.reviewed_item = self.content_type.get_object_for_this_type(
                pk=kwargs.get('object_id'))
        except ObjectDoesNotExist:
            raise Http404

        # Check for permission
        if request.user.is_authenticated():
            # Check, if user has already reviewed this item
            if getattr(settings, 'REVIEW_AVOID_MULTIPLE_REVIEWS', False):
                try:
                    old_review = Review.objects.filter(
                        user=request.user, content_type=self.content_type,
                        object_id=kwargs.get('object_id'))[0]
                except IndexError:
                    pass
                else:
                    return HttpResponseRedirect(
                        reverse('review_update', kwargs={'pk': old_review.pk}))
            # Check the custom permission function
            has_perm = getattr(settings, 'REVIEW_PERMISSION_FUNCTION', None)
            if (callable(has_perm)
                    and not has_perm(request.user, self.reviewed_item)):
                raise Http404
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)


class ReviewDetailView(DetailView):
    """View to display a ``Review`` instance."""
    model = Review


class ReviewUpdateView(ReviewViewMixin, ReviewUpdateMixin, UpdateView):
    """View to update a ``Review`` instance."""
    pass


class ReviewDeleteView(ReviewViewMixin, ReviewUpdateMixin, DeleteView):
    """View to delete a ``Review`` instance."""
    def get_success_url(self):
        if getattr(settings, 'REVIEW_DELETION_SUCCESS_URL', False):
                return reverse(settings.REVIEW_DELETION_SUCCESS_URL)
        return '/'
