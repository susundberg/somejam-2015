from django.contrib import admin
import chat_event.models

class EventAdmin(admin.ModelAdmin):
    list_display = ('chat', 'open', 'close')
    list_filter = ('chat', )
    
    
    
admin.site.register(chat_event.models.Event,EventAdmin )
