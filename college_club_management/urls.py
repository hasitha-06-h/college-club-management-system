"""
URL configuration for college_club_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# college_club_management/urls.py

# college_club_management/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home # Make sure this import is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # User authentication and profiles
    path('clubs/', include('clubs.urls')),       # Club management
    path('events/', include('events.urls')),     # Event management and calendar
    path('announcements/', include('announcements.urls')), # Announcements
    path('feedback/', include('feedback.urls')), # Rating and Feedback
    path('', home, name='home'), # <--- THIS LINE IS CRUCIAL FOR YOUR HOME PAGE
    
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This is for static files during development; in production, web server handles it.
    # Commented out to fix 404 errors for static files in development
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
