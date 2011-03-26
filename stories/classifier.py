import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import os

from models import CleanStory

def getFearWords():
    path = os.path.join(os.path.dirname(__file__), "fearwords.txt") 
    wordList = []
    with open(path) as words:
        for line in words:
            wordList.append(line.strip())
    return dict(map(lambda x: (x, 1), wordList))

FEARWORDS = getFearWords()

def word_feats(words):
    feats = dict([(word, True) for word in words])

    numFearWords = 0
    for word in words:
        if FEARWORDS.has_key(word.lower()):
            numFearWords += 1
    feats['num_fear_words'] = numFearWords
    return feats

def train():
    posStories = CleanStory.objects.filter(fearful=False)
    negStories = CleanStory.objects.filter(fearful=True)

    negfeats = [(word_feats(story.text.split()), 'neg') for story in negStories]
    posfeats = [(word_feats(story.text.split()), 'pos') for story in posStories]
         
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
         
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
         
    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()
