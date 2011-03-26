"Register the NewsSource model with the Admin application"
from django.contrib import admin
from models import *

class CleanStoryAdmin(admin.ModelAdmin):
    pass
    
class WebStoryAdmin(admin.ModelAdmin):
    pass

class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(NewsSource, NewsSourceAdmin)
admin.site.register(CleanStory, CleanStoryAdmin)
admin.site.register(WebStory, WebStoryAdmin)
