

# Create your models here.
# clubs/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation # For feedback app

class Club(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255) # Max length for slug
    description = models.TextField()
    # Using AUTH_USER_MODEL for members
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_clubs', blank=True)
    photo = models.ImageField(upload_to='club_photos/', blank=True, null=True)
    # Manager: A club officer assigned to manage this club.
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_clubs',
        limit_choices_to={'user_type': 'club_officer'} # Only allow club officers to be managers
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generic relations for feedback and ratings
    ratings = GenericRelation('feedback.Rating')
    feedback = GenericRelation('feedback.Feedback')


    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('club_detail', kwargs={'slug': self.slug})

class ClubMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club') # A user can join a club only once

    def __str__(self):
        return f"{self.user.username} - {self.club.title}"