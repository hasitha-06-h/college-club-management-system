from django.contrib import admin

# Register your models here.
# events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'club', 'created_by', 'is_upcoming')
    list_filter = ('date', 'club', 'created_by')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
