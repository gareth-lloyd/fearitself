import unittest
from googlereader import *
import feedparser
from datetime import datetime
import os
from models import NewsSource

class GoogleReaderTest(unittest.TestCase):
    def testCredentials(self):
        c = getCredentials()
        self.assertEqual("glloyd", c[0])

    def testInit(self):
        reader = Reader(getCredentials())
        self.assertTrue(reader.headers) 

    def testGetFeed(self):
        reader = Reader(getCredentials())
        u = "http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588"
        r = reader.getFeed(u)
        feed = feedparser.parse(r)

        for entry in feed.entries:
            print entry.title.encode('utf-8')

    def testGetFeedItemsAfter(self):
        reader = Reader(getCredentials())
        u = "http%3A%2F%2Fwww.thisislondon.co.uk%2Fstandard-home%2Frss%2F%3Fito%3D1588"
        r = reader.getFeedItemsAfter(u, datetime.now())
        feed = feedparser.parse(r)
        self.assertEqual(0, len(feed.entries))


from story_processor import * 
class StoryProcessorTest(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "testdata/feedentry.xml")
        with open(path) as feed:
            self.testdata = feed.read()

    def test(self):
        "The story processor should parse feed"
        sp = StoryProcessor()
        entries = sp.getEntries(self.testdata)
        self.assertEqual(1, len(entries))

    def testParseEntry(self):
        "should turn an entry into a WebStory by fetching"
        sp = StoryProcessor()
        source = NewsSource()
        entries = sp.getEntries(self.testdata)
        story = sp.processEntry(entries[0], source)
        self.assertTrue(hasattr(story, "fullText"))
        link = "http://telegraph.feedsportal.com/c/32726/f/564430/s/139f1592/l/0L0Stelegraph0O0Cculture0Ctvandradio0Cbbc0C840A610A70CBBC0Eaxes0EMy0EFamily0Esitcom0Eafter0Emore0Ethan0E10A0A0Eepisodes0Bhtml/story01.htm"
        self.assertEqual(link, story.link)
        date = datetime.strptime("2011-03-25T10:57:35Z", StoryProcessor.D_FMT)
        self.assertEqual(date, story.date)
        title = 'BBC axes My Family sitcom after more than 100 episodes'
        self.assertEqual(title, story.title)

