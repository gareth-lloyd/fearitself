#!/usr/bin/env python

from stories.googlereader import Reader, getCredentials
from stories.story_processor import saveStories
from stories.models import *
from django.core.management import setup_environ
import settings
from stories.newssources import *

def populate():
    r = Reader(getCredentials())
    
    for source in sources:
        saveStories(r.getFeed(source.feed), source)

if __name__ == "__main__":
    setup_environ(settings)
    populate()
