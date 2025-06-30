from django.contrib import admin
from .models import ChatModel

@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'room', 'timestamp', 'is_read')
    list_filter = ('sender', 'receiver', 'is_read')
    search_fields = ('message', 'room')
    ordering = ('-timestamp',)