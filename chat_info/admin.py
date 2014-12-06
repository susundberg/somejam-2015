from django.contrib import admin
import chat_info.models

admin.site.register(chat_info.models.Chat)
admin.site.register(chat_info.models.ChatType)