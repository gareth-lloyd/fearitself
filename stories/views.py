from django.template import RequestContext
from models import NewsSource, WebStory, CleanStory
from django.http import HttpResponse, HttpResponseRedirect
from forms import *

# Create your views here.
def fear(request):
    pass

def sources(request):
    sources = NewsSource.objects
    return render_to_response('charts.html',
          {'charts' : charts},
            context_instance=RequestContext(request))


def initsource(request, source_id=None):
    pass
