"""Template tags for the ``review`` app."""
from django.contrib.contenttypes.models import ContentType
from django.template import Library

from .. import models


register = Library()


@register.assignment_tag
def total_review_average(obj, normalize_to=100):
    """Returns the average for all reviews of the given object."""
    ctype = ContentType.objects.get_for_model(obj.__class__)
    total_average = 0
    reviews = models.Review.objects.filter(
        content_type=ctype, object_id=obj.id)
    for review in reviews:
        total_average += review.get_average_rating(normalize_to)
    if reviews:
        total_average /= reviews.count()
    return total_average


@register.assignment_tag
def user_has_reviewed(obj, user):
    """Returns True if the user has already reviewed the object."""
    ctype = ContentType.objects.get_for_model(obj.__class__)
    try:
        models.Review.objects.get(user=user, content_type=ctype,
                                  object_id=obj.id)
    except models.Review.DoesNotExist:
        return False
    return True
