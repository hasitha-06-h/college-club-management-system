from django.db import models

# Create your models here.
# events/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone
from clubs.models import Club # Assuming you have a Club model
from django.conf import settings # To link to your CustomUser model

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Event date and time
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # Link to the club that is hosting the event (optional: if events can exist without a club, make null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    
    # Who created the event (e.g., a club manager or admin)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_events')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time'] # Order events by date, then time
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} on {self.date.strftime('%Y-%m-%d')}"

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk}) # You'll define 'event_detail' later

    def is_past_event(self):
        """Checks if the event date is in the past."""
        return self.date < timezone.localdate()

    def is_upcoming(self):
        """Checks if the event date is today or in the future."""
        return self.date >= timezone.localdate()

    def get_display_date(self):
        """Returns date formatted nicely, e.g., 'Jul 25, 2025'"""
        return self.date.strftime('%b %d, %Y')

    def get_display_time(self):
        """Returns time formatted nicely, e.g., '03:30 PM'"""
        if self.time:
            return self.time.strftime('%I:%M %p')
        return "N/A"