from django.contrib import admin

# Register your models here.
# announcements/admin.py
from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_global', 'club', 'author', 'created_at', 'updated_at')
    list_filter = ('is_global', 'club', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'club__title')
    date_hierarchy = 'created_at' # Allows filtering by date in admin
    raw_id_fields = ('author', 'club') # Use raw_id_fields for FKs if you have many users/clubs

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Targeting', {
            'fields': ('is_global', 'club'),
            'description': 'If global, leave Club blank. If club-specific, select a club.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Makes this section collapsible in admin
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Automatically set the author to the current logged-in user when creating
        if not obj: # Only for new objects
            form.base_fields['author'].initial = request.user
            # If the user is a Club Manager, limit choices to clubs they manage
            if hasattr(request.user, 'user_type') and request.user.user_type == 'club_manager':
                form.base_fields['club'].queryset = request.user.managed_clubs.all()
        return form

    # Admin validation for club and is_global fields
    def clean(self):
        cleaned_data = super().clean()
        is_global = cleaned_data.get('is_global')
        club = cleaned_data.get('club')

        if is_global and club:
            self.add_error('club', 'A global announcement cannot be assigned to a specific club.')
        elif not is_global and not club:
            self.add_error('club', 'A club-specific announcement must have a club selected.')
        return cleaned_data