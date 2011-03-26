"Register the NewsSource model with the Admin application"
from django.contrib import admin
from models import NewsSource 

class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(NewsSource, NewsSourceAdmin)
