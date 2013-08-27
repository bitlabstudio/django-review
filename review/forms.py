"""Forms for the ``review`` app."""
from django import forms
from django.utils.translation import get_language

from .models import Review


class ReviewForm(forms.ModelForm):
    def __init__(self, reviewed_item, user=None, *args, **kwargs):
        self.user = user
        self.reviewed_item = reviewed_item
        super(ReviewForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.reviewed_item = self.reviewed_item
            self.instance.language = get_language()
        return super(ReviewForm, self).save(*args, **kwargs)

    class Meta:
        model = Review
        fields = ('content', )
