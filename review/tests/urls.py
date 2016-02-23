"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import ListView

from ..models import Review


admin.autodiscover()

urlpatterns = [
    url(r'^review-listing/', ListView.as_view(model=Review),
        name='review_list'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^umedia/', include('user_media.urls')),
    url(r'^review/', include('review.urls')),
]
