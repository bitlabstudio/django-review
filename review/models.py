"""Just an empty models file to let the testrunner recognize this as app."""
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields

DEFAULT_CHOICES = (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)


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
    :extra_item: Optional object, which should be attached to the review.

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

    # GFK 'extra_item'
    extra_content_type = models.ForeignKey(
        ContentType,
        related_name='reviews_attached',
        null=True, blank=True,
    )
    extra_object_id = models.PositiveIntegerField(null=True, blank=True)
    extra_item = generic.GenericForeignKey(
        'extra_content_type', 'extra_object_id')

    class Meta:
        ordering = ['-creation_date']

    def __unicode__(self):
        return '{0} - {1}'.format(self.reviewed_item, self.get_user())

    # TODO: Add magic to get ReviewExtraInfo content objects here

    def get_user(self):
        """Returns the user who wrote this review or ``Anonymous``."""
        if self.user:
            return self.user.email
        return ugettext('Anonymous')

    def get_averages(self, max_value=None):
        """
        Centralized average calculation. Returns category averages and total
        average.

        :param max_value: By default the app is set to a rating from 1 to 5.
          So if nothing is changed, we can just calculate the average of all
          rating values and be good. We then have an average that is between 1
          and 5 as well.
          BUT if  we have custom choices, we could end up having one category
          with a range of 1 to 10 and one category with 1 to 5. The result then
          must be abstracted to fit into the given range set by max_value.

          This can also be used to calculate percentages by setting max_value
          to 100.

        """
        max_rating_value = 0
        category_maximums = {}
        category_averages = {}
        categories = RatingCategory.objects.filter(counts_for_average=True,
                                                   rating__review=self)
        # find the highest rating possible across all categories
        for category in categories:
            category_max = category.get_rating_max_from_choices()
            category_maximums.update({category: category_max})
            if max_value is not None:
                max_rating_value = max_value
            else:
                if category_max > max_rating_value:
                    max_rating_value = category_max
        # calculate the average of every distinct category, normalized to the
        # recently found max
        for category in categories:
            category_average = None
            ratings = Rating.objects.filter(
                review=self,
                category=category, value__isnull=False).exclude(value='')
            category_max = category_maximums[category]
            for rating in ratings:
                if category_average is None:
                    category_average = float(rating.value)
                else:
                    category_average += float(rating.value)

            if category_average is not None:
                category_average *= float(max_rating_value) / float(
                    category_max)
                category_averages[category] = (
                    category_average / ratings.count())

        # calculate the total average of all categories
        total_average = 0
        for category, category_average in category_averages.iteritems():
            total_average += category_average
        if not len(category_averages):
            return (False, False)
        total_average /= len(category_averages)

        return total_average, category_averages

    def get_average_rating(self, max_value=None):
        """
        Returns the average rating for all categories of this review.

        A shortcut for get_averages. Look there for more details.

        """
        total_average, category_averages = self.get_averages(
            max_value=max_value)
        return total_average

    def get_category_averages(self, max_value=None):
        """
        Returns the average ratings for every category of this review.

        A shortcut for get_averages. Look there for more details.

        """
        total_average, category_averages = self.get_averages(
            max_value=max_value)
        return category_averages

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
        return '{0} - {1}'.format(self.review, self.type)


class RatingCategory(TranslatableModel):
    """
    Represents a rating category.

    If your reviews are just text based, you don't have to use this.

    This can be useful if you want to allow users to rate one or more
    categories, like ``Food``, ``Room service``, ``Cleansines`` and so on.

    :identifier: Optional identifier.
    :name: Name of the category. Also used as label for the category form.
    :question: If you want to render a more explicit question in addition to
      the name, use this field. It is added to the form fields as help text.
    :counts_for_average: If True, the ratings of this category will be used to
      calculate the average rating. Default is True.

    """
    identifier = models.SlugField(
        max_length=32,
        verbose_name=_('Identifier'),
        blank=True,
    )

    counts_for_average = models.BooleanField(
        verbose_name=_('Counts for average rating'),
        default=True,
    )

    translations = TranslatedFields(
        name=models.CharField(max_length=256),
        question=models.CharField(max_length=512, blank=True, null=True),
    )

    def __unicode__(self):
        return self.lazy_translation_getter('name', 'Untranslated')

    @property
    def required(self):
        """Returns False, if the choices include a None value."""
        if not hasattr(self, '_required'):
            # get_choices sets _required
            self.get_choices()
        return self._required

    def get_choices(self):
        """Returns the tuple of choices for this category."""
        choices = ()
        self._required = True
        for choice in self.choices.all():
            if choice.value is None or choice.value == '':
                self._required = False
            choices += (choice.value, choice.label),
        if not choices:
            return DEFAULT_CHOICES
        return choices

    def get_rating_max_from_choices(self):
        """Returns the maximun value a rating can have in this catgory."""
        return int(list(self.get_choices())[0][0])


class RatingCategoryChoice(TranslatableModel):
    """
    Defines an optional choice for a `RatingCategory`.

    If `RatingChoice` exists, the choices will not be loaded from the settings.

    :label: The label that is displayed for this choice.
    :ratingcategory: The `RatingCategory` this choice belongs to.
    :value: The value that this choice has. If a `RatingChoice` with value=None
      is created and chosen by the user, this category is not taken into
      account when the average is calculated.

    """
    ratingcategory = models.ForeignKey(
        RatingCategory,
        verbose_name=_('Rating category'),
        related_name='choices',
    )

    value = models.CharField(
        verbose_name=_('Value'),
        max_length=20,
        blank=True, null=True,
    )

    translations = TranslatedFields(
        label=models.CharField(
            verbose_name=_('Label'),
            max_length=128,
        ),
    )

    def __unicode__(self):
        return self.lazy_translation_getter('label',
                                            self.ratingcategory.identifier)

    class Meta:
        ordering = ('-value', )


class Rating(models.Model):
    """
    Represents a rating for one rating category.

    :rating: Rating value.
    :review: The review the rating belongs to.
    :category: The rating category the rating belongs to.

    """
    rating_choices = DEFAULT_CHOICES

    value = models.CharField(
        max_length=20,
        verbose_name=_('Value'),
        choices=getattr(settings, 'REVIEW_RATING_CHOICES', rating_choices),
        blank=True, null=True,
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
        return '{0}/{1} - {2}'.format(self.category, self.review, self.value)
