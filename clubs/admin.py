from django.contrib import admin

# Register your models here.
# clubs/admin.py
from django.contrib import admin
from .models import Club, ClubMembership

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'manager_username', 'photo_preview', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'manager__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('members',) # For easier management of many-to-many members
    list_filter = ('manager',) # Filter by manager

    def photo_preview(self, obj):
        if obj.photo:
            return '<img src="%s" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />' % obj.photo.url
        return "No Image"
    photo_preview.allow_tags = True
    photo_preview.short_description = 'Photo'

    def manager_username(self, obj):
        return obj.manager.username if obj.manager else "N/A"
    manager_username.short_description = 'Manager'

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'date_joined')
    list_filter = ('club', 'user')
    search_fields = ('user__username', 'club__title')
    raw_id_fields = ('user', 'club') # Use raw ID for performance with many users/clubs
