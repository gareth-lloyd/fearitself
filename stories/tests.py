"""
This is not real TDD, but more like interacting with my
code as I write it. Sort of ad-hoc integration tests. 
Hey, it's a hack day.
"""
import chardet
import unittest
from googlereader import *
import feedparser
from datetime import datetime
import os
from models import NewsSource

class GoogleReaderTest(unittest.TestCase):
    u = "http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588"
    def testCredentials(self):
        c = getCredentials()
        self.assertEqual("glloyd", c[0])

    def testInit(self):
        reader = Reader(getCredentials())
        self.assertTrue(reader.headers) 

    def testGetFeed(self):
        reader = Reader(getCredentials())
        r = reader.getFeed(GoogleReaderTest.u)
        feed = feedparser.parse(r)

        for entry in feed.entries:
            print entry.title.encode('utf-8')

    def testGetFeedItemsAfter(self):
        reader = Reader(getCredentials())
        r = reader.getFeedItemsAfter(GoogleReaderTest.u, datetime.now())
        feed = feedparser.parse(r)
        self.assertEqual(0, len(feed.entries))

    def testGetFeedItemsAfterRepeated(self):
        reader = Reader(getCredentials())
        oldDate = datetime(2011, 3, 25)
        continuation = None
        while True:
            response = reader.getFeedItemsAfter(GoogleReaderTest.u, oldDate, continuation)
            content = response.read()
            continuation = reader.getContinuation(content)
            entries = feedparser.parse(content).entries
            if len(entries) < 20:
                break
            for e in entries:
                print e.published

from story_processor import * 
class StoryProcessorTest(unittest.TestCase):
    def testData(self, name="feedentry.xml"):
        path = os.path.join(os.path.dirname(__file__), "testdata/%s" % name)
        with open(path) as feed:
            contents = feed.read()
        return contents

    def test(self):
        "The story processor should parse feed"
        entries = getEntries(self.testData())
        self.assertEqual(1, len(entries))

    def testParseEntry(self):
        "should turn an entry into a WebStory by fetching"
        source = NewsSource()
        entries = getEntries(self.testData())
        story = processEntry(entries[0], source)
        self.assertTrue(hasattr(story, "fullText"))
        link = "http://telegraph.feedsportal.com/c/32726/f/564430/s/139f1592/l/0L0Stelegraph0O0Cculture0Ctvandradio0Cbbc0C840A610A70CBBC0Eaxes0EMy0EFamily0Esitcom0Eafter0Emore0Ethan0E10A0A0Eepisodes0Bhtml/story01.htm"
        self.assertEqual(link, story.link)
        date = datetime.strptime("2011-03-25T10:57:35Z", D_FMT)
        self.assertEqual(date, story.date)
        title = 'BBC axes My Family sitcom after more than 100 episodes'
        self.assertEqual(title, story.title)

    def testProcessRss(self):
        source = NewsSource(name="name", feed="feed")
        source.save()
        feedContents = self.testData("readernews.xml")
        saveStories(feedContents, source)

        print len(WebStory.objects)

from classifier import *
class ClassifierTest(unittest.TestCase):
    def test(self):
        pass
