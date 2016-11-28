"""Template tags for the ``review`` app."""
from django.contrib.contenttypes.models import ContentType
from django.template import Library

from .. import models


register = Library()


@register.assignment_tag
def get_reviews(obj):
    """Simply returns the reviews for an object."""
    ctype = ContentType.objects.get_for_model(obj)
    return models.Review.objects.filter(content_type=ctype, object_id=obj.id)


@register.assignment_tag
def get_review_average(obj):
    """Returns the review average for an object."""
    total = 0
    reviews = get_reviews(obj)
    if not reviews:
        return False
    for review in reviews:
        average = review.get_average_rating()
        if average:
            total += review.get_average_rating()
    if total > 0:
        return total / reviews.count()
    return False


@register.assignment_tag
def get_review_count(obj):
    """Simply returns the review count for an object."""
    return get_reviews(obj).count()


@register.inclusion_tag('review/partials/category_averages.html')
def render_category_averages(obj, normalize_to=100):
    """Renders all the sub-averages for each category."""
    context = {'reviewed_item': obj}
    ctype = ContentType.objects.get_for_model(obj)
    reviews = models.Review.objects.filter(
        content_type=ctype, object_id=obj.id)
    category_averages = {}
    for review in reviews:
        review_category_averages = review.get_category_averages(normalize_to)
        if review_category_averages:
            for category, average in review_category_averages.items():
                if category not in category_averages:
                    category_averages[category] = review_category_averages[
                        category]
                else:
                    category_averages[category] += review_category_averages[
                        category]
    if reviews and category_averages:
        for category, average in category_averages.items():
            category_averages[category] = \
                category_averages[category] / models.Rating.objects.filter(
                    category=category, value__isnull=False,
                    review__content_type=ctype,
                    review__object_id=obj.id).exclude(value='').count()
    else:
        category_averages = {}
        for category in models.RatingCategory.objects.filter(
                counts_for_average=True):
            category_averages[category] = 0.0
    context.update({'category_averages': category_averages})
    return context


@register.assignment_tag
def total_review_average(obj, normalize_to=100):
    """Returns the average for all reviews of the given object."""
    ctype = ContentType.objects.get_for_model(obj)
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
    ctype = ContentType.objects.get_for_model(obj)
    try:
        models.Review.objects.get(user=user, content_type=ctype,
                                  object_id=obj.id)
    except models.Review.DoesNotExist:
        return False
    return True
