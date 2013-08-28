"""Forms for the ``review`` app."""
from django import forms
from django.conf import settings
from django.utils.translation import get_language

from .models import Review, Voting, VotingCategory


class ReviewForm(forms.ModelForm):
    def __init__(self, reviewed_item, user=None, *args, **kwargs):
        self.user = user
        self.reviewed_item = reviewed_item
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Dynamically add fields for each voting category
        for category in VotingCategory.objects.all():
            self.fields['category_{}'.format(category.pk)] = forms.ChoiceField(
                choices=getattr(settings, 'REVIEW_VOTE_CHOICES',
                                Voting.vote_choices),
                label=category.get_translation().name,
            )

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.reviewed_item = self.reviewed_item
            self.instance.language = get_language()
        self.instance = super(ReviewForm, self).save(*args, **kwargs)
        for field in self.fields:
            if field.startswith('category_'):
                voting, created = Voting.objects.get_or_create(
                    review=self.instance,
                    category=VotingCategory.objects.get(
                        pk=field.replace('category_', '')),
                )
                voting.vote = self.cleaned_data[field]
                voting.save()
        return self.instance

    class Meta:
        model = Review
        fields = ('content', )
