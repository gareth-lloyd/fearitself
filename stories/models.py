from django.db import models

class NewsSource(models.Model):
    """
    Organization/publication publishing news in an 
    RSS feed. 
    """
    name = models.CharField(blank=False, max_length=300)
    feed = models.CharField(blank=False, max_length=255, unique=True)
    lastAccessed = models.DateTimeField(blank=True, null=True)
    
class WebStory(models.Model):
    """
    Full text of a story retrieved from a news website, 
    with no attempt to make sense of HTML etc.
    """
    title = models.CharField(blank=False, max_length=300)
    link = models.CharField(blank=False, max_length=600)
    date = models.DateField(blank=False)
    source = models.ForeignKey(NewsSource)
    fullText = models.TextField(blank=False)

    class Meta:
        unique_together = (('title', 'source'),)

class CleanStory(models.Model):
    fearful = models.NullBooleanField()
    webStory = models.OneToOneField(WebStory, primary_key=True)
    text = models.TextField(blank=False)
