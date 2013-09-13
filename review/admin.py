"""Admin classes for the review app."""
from django.contrib import admin

from simple_translation.admin import TranslationAdmin

from . import models


class RatingAdmin(admin.ModelAdmin):
    list_display = ['review', 'category', 'value', ]
    raw_id_fields = ['review', ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user', 'language', 'creation_date']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.RatingCategory, TranslationAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.ReviewExtraInfo, ReviewExtraInfoAdmin)
