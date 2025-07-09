from django.db import models

# Create your models here.
# feedback/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    """
    Model for user ratings, using GenericForeignKey to rate any content type.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5 stars."
    )
    # Generic Foreign Key to link to any content type (e.g., Club, Event)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id') # One rating per user per object
        ordering = ['-created_at'] # Order by most recent

    def __str__(self):
        # Ensure content_object is not None before accessing its attributes
        content_name = self.content_object.title if hasattr(self.content_object, 'title') else str(self.content_object)
        return f"{self.user.username} rated {content_name} as {self.rating} stars"

class Feedback(models.Model):
    """
    Model for user text feedback/comments, also using GenericForeignKey.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_feedback')
    comment = models.TextField(help_text="Share your thoughts and feedback.")
    # Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Order by most recent

    def __str__(self):
        content_name = self.content_object.title if hasattr(self.content_object, 'title') else str(self.content_object)
        return f"Feedback by {self.user.username} on {content_name}: {self.comment[:50]}..."
