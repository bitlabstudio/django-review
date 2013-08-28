"""Admin classes for the review app."""
from django.contrib import admin

from simple_translation.admin import TranslationAdmin

from . import models


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user', 'language', 'creation_date']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.ReviewExtraInfo, ReviewExtraInfoAdmin)
admin.site.register(models.RatingCategory, TranslationAdmin)
