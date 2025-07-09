

# Create your models here.
# announcements/models.py
# announcements/models.py
from django.db import models
from django.conf import settings # To link to your CustomUser model
from clubs.models import Club # To link to a specific club

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Who created the announcement
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='posted_announcements')
    
    # Is this a global announcement (for everyone) or specific to a club?
    is_global = models.BooleanField(default=True, help_text="Check if this announcement is for all users.")
    
    # If not global, link to the specific club it belongs to
    # 'null=True, blank=True' allows it to be global (no club)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, related_name='club_announcements',
                             help_text="Leave blank for a global announcement. Select a club for a club-specific announcement.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Order by most recent first
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        if self.is_global:
            return f"[Global] {self.title} by {self.author.username}"
        else:
            return f"[{self.club.title}] {self.title} by {self.author.username}"

    def get_absolute_url(self):
        # Define a detail URL if you want individual announcement pages
        from django.urls import reverse
        return reverse('announcement_detail', kwargs={'pk': self.pk})