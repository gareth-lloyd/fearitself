from django import forms
from models import CleanStory


class TrainingForm(forms.ModelForm):
    class Meta:
        model = CleanStory
        exclude = ('webStory')
