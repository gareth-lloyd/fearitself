from django.template import RequestContext
from models import NewsSource, WebStory, CleanStory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from googlereader import Reader, getCredentials
from datetime import datetime, date
from story_processor import saveStories
from forms import TrainingForm

START = datetime(2011, 3, 21)

class FearLevel(object):
    def __init__(self, name, colourName, low, high):
        self.name = name
        self.colour = colourName
        self.low = low
        self.high = high

    def setActive(self, level):
        if self.low < level <= self.high:
            self.active = True
        else:
            self.active = False

LEVELS = [
    FearLevel('shit it..', 'red',  .4, 1.0),
    FearLevel('panic buy', 'orange', .35, .4),
    FearLevel('an ill wind', 'yellow', .30, .35),
    FearLevel('carry on', 'green', .25, .2),
    FearLevel('pimms anyone?', 'blue', 0, .25),
]

def fear(request):
    "State the level of fear"    
    fearful = 0.0
    nonfearful = 0.0
    stories = WebStory.objects.filter(date__gte=date.today())
    for story in stories:
        fear = story.cleanstory.fearful
        if fear == 1:
            fearful+= 1
        elif fear == 0:
            nonfearful += 1
    denominator = (fearful + nonfearful)
    if denominator > 0:
        fearlevel = fearful / denominator
    else: 
        fearlevel = 0
    print "Threat level: %s fearful %s nonfearful %s" %(fearlevel, fearful, nonfearful)
    return render_to_response('fear.html',
            {'levels': getLevels(fearlevel)},
            context_instance=RequestContext(request))

# this is never used to create new CleanStory objects
def training(request, clean_id=None):
        
    if request.method == 'POST':
        print "POST"
        instance = get_object_or_404(CleanStory, pk=clean_id)
        form = TrainingForm(request.POST, instance=instance)
        cleanStory = form.save()
    
    if request.method == 'GET' and clean_id is not None:
        instance = get_object_or_404(CleanStory, pk=clean_id)
    else:
        # get next unclassified
        stories = CleanStory.objects.all()
        for s in stories:
            if s.fearful is None:
                instance = s
        if not s:
            return HttpResponseRedirect('/fear/sources/')
    form = TrainingForm(instance=instance)
    return render_to_response('training.html',
                    {'form': form, 'cleanStory': instance},
                    context_instance=RequestContext(request))

def getLevels(fearlevel):
    for level in LEVELS:
        level.setActive(fearlevel)
    return LEVELS

def sources(request):
    sources = NewsSource.objects.all()
    return render_to_response('sources.html',
          {'sources' : sources},
            context_instance=RequestContext(request))

def updatesource(request, source_id=None):
    source = NewsSource.objects.get(id=source_id)
    start = source.lastAccessed
    if not start:
        start = START
    getFeedItems(source, start)
    return HttpResponseRedirect('/fear/sources/')

def getFeedItems(source, start):
    reader = Reader(getCredentials())
    continuation = None
    while True:
        response = reader.getFeedItemsAfter(source.feed, start, continuation)
        content = response.read()
        continuation = reader.getContinuation(content)
        lastDate = saveStories(content, source)
        source.lastAccessed = lastDate
        source.save()
