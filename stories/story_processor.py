from models import WebStory, CleanStory
from django.db import IntegrityError
import chardet
from datetime import datetime
from urllib2 import Request, urlopen
from BeautifulSoup import BeautifulSoup
import feedparser

D_FMT = '%Y-%m-%dT%H:%M:%SZ'

def saveStories(feedContents, source):
    entries = getEntries(feedContents)
    for entry in entries:
        try:
            story = WebStory.objects.get(title=entry.title, source=source)
        except :
            story = None
        if story:
            print "FOUND existing story"
        else:
            story = processEntry(entry, source)
            print 'Saving: %s' % story.title
            try:
                story.save()
            except IntegrityError:
                print "WARNING. Skipped duplicate entry for %s" % story.title
        lastDate = story.date
    return lastDate

def getEntries(feedContents):
    feed = feedparser.parse(feedContents)
    return feed.entries

def getFullText(link):
    request = Request(link)
    content = urlopen(request).read()
    encoding = chardet.detect(content)['encoding']
    return unicode(content, encoding)

def processEntry(entry, source):
    link = entry.link
    fullText = getFullText(link)
    date = datetime.strptime(entry.published, D_FMT)
    return WebStory(title=entry.title, 
            link=link, date=date,
            source=source, fullText=fullText)

def cleanStory(story):
    soup = BeautifulSoup(story.fullText)
    paras = soup.findAll('p')
    texts = [story.title]
    for p in paras:
        texts.append(_processPara(p))
    
    cleanText = " ".join(texts)
    return CleanStory(text=cleanText, webStory=story)

def _processPara(p):
    text = p.getText()
    if len(text) > 30:
        return text
    else:
        return ''

