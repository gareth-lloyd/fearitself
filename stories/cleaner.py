from BeautifulSoup import BeautifulSoup
from models import *
from newssources import *

def clean(webStory):
    soup = BeautifulSoup(webStory.fullText)
    texts = [webStory.title]
    
    print "Cleaning "+webStory.source.name+" article: "+webStory.title
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
                texts.append(introcopy.renderContents().encode('ascii'))
            bodycopy = soup.find('p', {'id': 'bodycopy'})
            if (bodycopy):
                texts.append(bodycopy.renderContents().encode('ascii'))
        except UnicodeDecodeError:
            print "bad text in "+webStory.link
            
    elif (webStory.source.id == standard.id):
        article = soup.find('div', { 'id': 'article'})
        if (article):
            paragraphs = article.findAll('p')
            for p in paragraphs:
                texts.append(_processPara(p))
                
    else:
        paras = soup.findAll('p')
        for p in paras:
            texts.append(_processPara(p))

    cleanText = " ".join(texts)
    return CleanStory(text=cleanText, webStory=webStory)

def _processPara(p):
    text = p.getText()
    if len(text) > 30:
        return text
    else:
        return ''