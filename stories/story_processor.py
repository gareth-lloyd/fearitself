from models import WebStory, CleanStory
from datetime import datetime
from urllib2 import Request, urlopen
from BeautifulSoup import BeautifulSoup
import feedparser


class StoryProcessor(object):
    D_FMT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self):
        pass

    def getEntries(self, feedContents):
        feed = feedparser.parse(feedContents)
        return feed.entries

    def processEntry(self, entry, source):
        link = entry.link
        fullText = urlopen(link).read()
        date = datetime.strptime(entry.published, StoryProcessor.D_FMT)
        return WebStory(title=entry.title, 
                link=link, date=date,
                source=source, fullText=fullText)

class StoryCleaner(object):
    def __init__(self):
        pass

    def cleanStory(self, story):
        soup = BeautifulSoup(story.fullText)
        paras = soup.findAll('p')
        texts = []
        for p in paras:
            texts.append(self._processPara(p))
        
        cleanText = " ".join(texts)
        return CleanStory(text=cleanText, webStory=story)

    def _processPara(self, p):
        text = p.getText()
        if len(text) > 30:
            return text
        else:
            return ''

