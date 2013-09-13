"""Just an empty models file to let the testrunner recognize this as app."""
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from django_libs.models_mixins import SimpleTranslationMixin


class Review(models.Model):
    """
    Represents a user review, which includes free text and images.

    :reviewed_item: Object, which is reviewed.
    :user (optional): User, which posted the rating.
    :content (optional): Running text.
    :images (optional): Review-related images.
    :language (optional): Language shortcut to filter reviews.
    :creation_date: The date and time, this review was created.
    :average_rating: Should always be calculated and updated when the object is
      saved. This is for improving performance and reducing db queries when
      calculating ratings for reviewed items. Currently it gets updated at the
      end of the save method of the ``ReviewForm``. This means that when you
      manually save a Review via the Django admin, this field will not be
      updated.

    """
    # GFK 'reviewed_item'
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reviewed_item = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        blank=True, null=True,
    )

    content = models.TextField(
        max_length=1024,
        verbose_name=_('Content'),
        blank=True,
    )

    images = generic.GenericRelation(
        'user_media.UserMediaImage',
    )

    language = models.CharField(
        max_length=5,
        verbose_name=_('Language'),
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    average_rating = models.FloatField(
        verbose_name=_('Average rating'),
        default=0,
    )

    class Meta:
        ordering = ['-creation_date']

    def __unicode__(self):
        return '{} - {}'.format(self.reviewed_item, self.get_user())

    # TODO: Add magic to get ReviewExtraInfo content objects here

    def get_user(self):
        """Returns the user who wrote this review or ``Anonymous``."""
        if self.user:
            return self.user.email
        return ugettext('Anonymous')

    def get_average_rating(self):
        """
        Returns the average rating for all categories of this review.

        This is useful if you have several ratings for different categories
        like ``Service``, ``Product Quality`` and want to show a total rating
        for this review.

        """
        if self.ratings.all():
            total = 0
            for rating in self.ratings.all():
                total += int(rating.value)
            return total / self.ratings.count()
        return False

    def is_editable(self):
        """
        Returns True, if the time period to update this review hasn't ended
        yet.

        If the period setting has not been set, it always return True. This
        is the general case. If the user has used this setting to define an
        update period it returns False, if this period has expired.

        """
        if getattr(settings, 'REVIEW_UPDATE_PERIOD', False):
            period_end = self.creation_date + timezone.timedelta(
                seconds=getattr(settings, 'REVIEW_UPDATE_PERIOD') * 60)
            if timezone.now() > period_end:
                return False
        return True


class ReviewExtraInfo(models.Model):
    """
    Model to add any extra information to a review.

    This can be useful if you need to save more information about a reviewer
    than just the User instance. Let's say you are building a site for theme
    park reviews and you want to allow the user to select the weather
    conditions for the day of his visit (which will surely influence his
    review). This model would allow you to tie any model of your app to a
    review.

    :type: Callable type of the extra info. This should be unique per review.
      We will soon add a hack to the Review model which allows you to get the
      content_object of this instance from a review instance (i.e. by calling
      ``my_review.weather_conditions.name``). So for this example you would
      set the type to ``weather_conditions``.
    :review: Related review.
    :content_object: The related object that stores this extra information.

    """
    type = models.CharField(
        max_length=256,
        verbose_name=_('Type'),
    )

    review = models.ForeignKey(
        'review.Review',
        verbose_name=_('Review'),
    )

    # GFK 'content_object'
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['type']

    def __unicode__(self):
        return '{} - {}'.format(self.review, self.type)


class RatingCategory(SimpleTranslationMixin, models.Model):
    """
    Represents a rating category.

    If your reviews are just text based, you don't have to use this.

    This can be useful if you want to allow users to rate one or more
    categories, like ``Food``, ``Room service``, ``Cleansines`` and so on.

    """
    def __unicode__(self):
        return self.get_translation().name


class RatingCategoryTranslation(models.Model):
    """
    Represents translations of the ``RatingCategory`` model.

    :name: Name of the category.

    """
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )

    # simple-translation fields
    category = models.ForeignKey(RatingCategory)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    """
    Represents a rating for one rating category.

    :rating: Rating value.
    :review: The review the rating belongs to.
    :category: The rating category the rating belongs to.

    """
    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    value = models.CharField(
        max_length=20,
        verbose_name=_('Value'),
        choices=getattr(settings, 'REVIEW_RATING_CHOICES', rating_choices),
    )

    review = models.ForeignKey(
        'review.Review',
        verbose_name=_('Review'),
        related_name='ratings',
    )

    category = models.ForeignKey(
        'review.RatingCategory',
        verbose_name=_('Category'),
    )

    class Meta:
        ordering = ['category', 'review']

    def __unicode__(self):
        return '{}/{} - {}'.format(self.category, self.review, self.value)
