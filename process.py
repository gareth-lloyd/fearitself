#!/usr/bin/env python

from stories.story_processor import saveStories
from stories.models import *
from django.core.management import setup_environ
import settings

def process():
    webStories = WebStory.objects.all()
    for story in webStories:
        print story

if __name__ == "__main__":
    setup_environ(settings)
    process()
