

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('club_officer', 'Club Officer'),
        ('college_admin', 'College Admin'), # Renamed for clarity vs Django's is_staff
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')

    # You can add more profile fields here if needed, e.g.:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # phone_number = models.CharField(max_length=15, blank=True)
    # date_of_birth = models.DateField(null=True, blank=True)

    def is_student(self):
        return self.user_type == 'student'

    def is_club_officer(self):
        return self.user_type == 'club_officer'

    def is_college_admin(self):
        # A college admin typically also has Django's is_staff or is_superuser flags
        return self.user_type == 'college_admin' or self.is_staff or self.is_superuser

    def __str__(self):
        return self.username