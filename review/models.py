"""Just an empty models file to let the testrunner recognize this as app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Review(models.Model):
    """
    Represents a user review, which includes running text and ratings.

    :reviewed_item: Object, which is reviewed.
    :user (optional): User, which posted the rating.
    :content (optional): Running text.
    :images (optional): Review-related images.
    :language (optional): Language shortcut to filter reviews.
    :creation_date: The date and time, this review was created.

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

    class Meta:
        ordering = ['-creation_date']

    def __unicode__(self):
        if self.user:
            user = self.user.email
        else:
            user = _('Anonymous')
        return '{} - {}'.format(self.reviewed_item, user)
