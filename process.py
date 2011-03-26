#!/usr/bin/env python

from stories.cleaner import clean
from stories.models import *
from django.core.management import setup_environ
import settings

def process():
    webStories = WebStory.objects.all()
    for story in webStories:
        cleaned = clean(story)
        current = CleanStory.objects.get(webStory=story)
        if (current):
            cleaned.fearful=current.fearful
        cleaned.save()

if __name__ == "__main__":
    setup_environ(settings)
    process()
