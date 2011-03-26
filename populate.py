#!/usr/bin/env python

from stories.googlereader import Reader, getCredentials
from stories.story_processor import saveStories
from stories.models import *
from django.core.management import setup_environ
import settings

STANDARD_URL= "http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588"
MAIL_URL = "http%3A%2F%2Fwww.dailymail.co.uk%2Fnews%2Findex.rss"

def populate():
    mail = NewsSource(name="Daily Mail", feed=MAIL_URL)
    mail.save()

    standard = NewsSource(name="Evening Standard", feed=STANDARD_URL)
    standard.save()

    r = Reader(getCredentials())
    saveStories(r.getFeed(MAIL_URL), mail)
    saveStories(r.getFeed(STANDARD_URL), standard)

if __name__ == "__main__":
    setup_environ(settings)
    populate()