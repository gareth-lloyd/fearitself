from BeautifulSoup import BeautifulSoup
from models import *
from newssources import *
import re

def clean(webStory):
    soup = BeautifulSoup(webStory.fullText)
    texts = [webStory.title]
    
    print "Cleaning "+webStory.source.name+" article: "+webStory.title+" - "+webStory.link
    if (webStory.source.id == dailymail.id):
        article = soup.find('div', {'id': 'js-article-text'})
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
        else:
            print "no article text for dailymail: "+webStory.link
        
    elif (webStory.source.id == dailystar.id):
        try:
            introcopy = soup.find('p', {'class': 'introcopy'})
            if (introcopy):
                texts.append(_strip(introcopy.renderContents().encode('ascii')))
        except UnicodeDecodeError:
            print "bad text in intro "+webStory.link
        try:
            bodycopy = soup.find('p', {'id': 'bodycopy'})
            if (bodycopy):
                texts.append(_strip(bodycopy.renderContents().encode('ascii')))
        except UnicodeDecodeError:
            print "bad text in body "+webStory.link
        
        stories = soup.findAll('p', {'class': 'storycopy'})
        for copy in stories:
            try:
                texts.append(_strip(copy.renderContents().encode('ascii')))
            except UnicodeDecodeError:
                print "bad text in storycopy "+webStory.link
            
    elif (webStory.source.id == standard.id):
        article = soup.find('div', { 'id': 'article'})
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    elif (webStory.source.id == mirror.id):
        article = soup.find('div', {'class': 'article-body'})
        
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    elif (webStory.source.id == telegraph.id):
        article = soup.find('div', {'id': 'mainBodyArea'})
        
        if (article):
            paragraphs = article.findAll('div')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    elif (webStory.source.id == express.id):
        paragraphs = soup.findAll('p', {'class': 'storycopy'})
        for p in paragraphs:
            texts.append(_processPara(p))
            
    elif (webStory.source.id == guardian.id):
        article = soup.find('div', {'id': 'article-body-blocks'})
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    elif (webStory.source.id == sun.id):
        article = soup.find('div', {'id': 'bodyText'})
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    else:
        print "Default cleaner for: "+webStory.link
        paras = soup.findAll('p')
        for p in paras:
            texts.append(_processPara(p))

    cleanText = " ".join(texts)
    return CleanStory(text=cleanText, webStory=webStory)
   
htmlPattern = re.compile(r'<.*?>')
whitespacePattern = re.compile(r'\s+')
def _strip(data):
    return htmlPattern.sub('', data)

def _processPara(p):
    return _strip(p.getText())