"""Views for the review app."""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, DetailView

from .forms import ReviewForm
from .models import Review


#------ MIXINS ------#

class ReviewViewMixin(object):
    model = Review
    form_class = ReviewForm

    def dispatch(self, request, *args, **kwargs):
        # Check, if user needs to be logged in
        if getattr(settings, 'REVIEW_ALLOW_ANONYMOUS', False):
            return super(ReviewViewMixin, self).dispatch(
                request, *args, **kwargs)
        return login_required(super(ReviewViewMixin, self).dispatch)(
            request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReviewViewMixin, self).get_form_kwargs(*args, **kwargs)
        kwargs.update({'reviewed_item': self.reviewed_item})
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('review_detail', kwargs={'pk': self.object.pk})


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

        # Check for permission
        if request.user.is_authenticated():
            # Check, if user has already reviewed this item
            if getattr(settings, 'REVIEW_AVOID_MULTIPLE_REVIEWS', False):
                try:
                    old_review = Review.objects.get(
                        user=request.user, content_type=self.content_type,
                        object_id=kwargs.get('object_id'))
                except Review.DoesNotExist:
                    pass
                else:
                    return HttpResponseRedirect(
                        reverse('review_detail', kwargs={'pk': old_review.pk}))
            # Check the custom permission function
            has_perm = getattr(settings, 'REVIEW_PERMISSION_FUNCTION', None)
            if callable(has_perm) and not has_perm(request.user):
                raise Http404

        # Check, if reviewed item exists
        try:
            self.reviewed_item = self.content_type.get_object_for_this_type(
                pk=kwargs.get('object_id'))
        except ObjectDoesNotExist:
            raise Http404
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)


class ReviewDetailView(DetailView):
    """View to display a ``Review`` instance."""
    model = Review
