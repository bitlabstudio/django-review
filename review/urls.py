"""URLs for the review app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/delete/$',
        views.ReviewDeleteView.as_view(),
        name='review_delete'),
    url(r'^(?P<pk>\d+)/update/$',
        views.ReviewUpdateView.as_view(),
        name='review_update'),
    url(r'^(?P<pk>\d+)/$',
        views.ReviewDetailView.as_view(),
        name='review_detail'),
    url(r'^(?P<content_type>[-\w]+)/(?P<object_id>\d+)/create/$',
        views.ReviewCreateView.as_view(),
        name='review_create'),
)
