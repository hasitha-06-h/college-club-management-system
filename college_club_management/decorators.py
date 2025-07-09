# college_club_management/decorators.py
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from functools import wraps # For @wraps

def college_admin_required(function):
    """
    Decorator for views that checks if the user is authenticated and is a college admin.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_college_admin():
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "You do not have permission to access this page. (College Admin Required)")
            return redirect(reverse_lazy('home')) # Redirect to home or specific forbidden page
    return wrap

def club_officer_required(function):
    """
    Decorator for views that checks if the user is authenticated and is a club officer.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_club_officer():
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "You do not have permission to access this page. (Club Officer Required)")
            return redirect(reverse_lazy('home'))
    return wrap


class CollegeAdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a college admin."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() # Redirects to login
        if not request.user.is_college_admin():
            messages.warning(request, "You do not have permission to access this page. (College Admin Required)")
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

class ClubOfficerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a club officer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() # Redirects to login
        if not request.user.is_club_officer():
            messages.warning(request, "You do not have permission to access this page. (Club Officer Required)")
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

class ClubManagerRequiredMixin(AccessMixin):
    """
    Mixin to check if the user is the manager of the specific club
    being accessed (e.g., for edit/delete club pages).
    Requires the view to have `slug` in kwargs.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        club_slug = kwargs.get('slug')
        if not club_slug:
            # Should not happen if URLs are correctly configured
            messages.error(request, "Club not found.")
            return redirect(reverse_lazy('club_list'))

        try:
            club = Club.objects.get(slug=club_slug)
            # A college admin can manage any club
            if request.user.is_college_admin():
                return super().dispatch(request, *args, **kwargs)
            # A club officer can manage only the club they are assigned to
            if request.user.is_club_officer() and club.manager == request.user:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.warning(request, "You do not have permission to manage this club.")
                return redirect(reverse_lazy('club_detail', kwargs={'slug': club_slug}))
        except Club.DoesNotExist:
            messages.error(request, "Club does not exist.")
            return redirect(reverse_lazy('club_list'))