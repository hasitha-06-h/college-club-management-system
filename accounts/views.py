from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from clubs.models import Club
from announcements.models import Announcement
from django.db.models import Avg, Count # For average rating and member count on home

def home(request):
    global_announcements = Announcement.objects.filter(is_global=True).order_by('-created_at')[:5]
    
    # Order featured clubs by average rating (if available) or by member count
    featured_clubs = Club.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        member_count=Count('members')
    ).order_by('-avg_rating', '-member_count')[:3] # Prioritize avg rating, then member count

    context = {
        'global_announcements': global_announcements,
        'featured_clubs': featured_clubs,
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto-login after signup
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your signup. Please correct the fields.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Default Django LoginView handles POST logic, just need template name
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, f'Welcome back, {user.username}!')
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})

# Use Django's built-in logout view directly in URLs
# @login_required
# def user_logout(request):
#     logout(request)
#     messages.info(request, 'You have been logged out.')
#     return redirect('home')