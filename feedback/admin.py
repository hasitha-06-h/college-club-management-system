from django.contrib import admin

# Register your models here.
# feedback/admin.py
from django.contrib import admin
from .models import Rating, Feedback

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating', 'created_at') # Note 'rating' here
    list_filter = ('content_type', 'rating', 'created_at')
    readonly_fields = ('user', 'created_at', 'content_type', 'object_id')
    search_fields = ('user__username',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'comment', 'created_at')
    list_filter = ('content_type', 'created_at')
    readonly_fields = ('user', 'created_at', 'content_type', 'object_id')
    search_fields = ('comment', 'user__username',)