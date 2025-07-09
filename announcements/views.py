# announcements/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q # For complex queries

from .models import Announcement
from .forms import AnnouncementForm
from clubs.models import Club # For filtering by club

# Custom Mixins for Permissions (assuming you have these or similar)
# college_club_management/decorators.py
# class CollegeAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_authenticated and self.request.user.user_type == 'college_admin'
#
# class ClubManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_authenticated and self.request.user.user_type == 'club_manager'


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 10 # Display 10 announcements per page

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter for global announcements
        q_global = Q(is_global=True)
        
        # Filter for announcements specific to clubs the user is involved with
        q_user_clubs = Q()
        if self.request.user.is_authenticated:
            # If user is a member of any club
            if hasattr(self.request.user, 'joined_clubs'): # Assuming your CustomUser has 'joined_clubs'
                user_club_ids = self.request.user.joined_clubs.values_list('id', flat=True)
                q_user_clubs |= Q(club__id__in=user_club_ids)

            # If user is a manager of any club
            if hasattr(self.request.user, 'managed_clubs'): # Assuming your CustomUser has 'managed_clubs'
                managed_club_ids = self.request.user.managed_clubs.values_list('id', flat=True)
                q_user_clubs |= Q(club__id__in=managed_club_ids)
            
            # If user is a College Admin, they see all announcements
            if hasattr(self.request.user, 'user_type') and self.request.user.user_type == 'college_admin':
                return queryset.order_by('-created_at') # Admins see all, no specific filter needed

        # Combine global and user-specific club announcements
        # Use .distinct() to prevent duplicates if an announcement matches multiple criteria
        return queryset.filter(q_global | q_user_clubs).order_by('-created_at').distinct()


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        # Ensure only relevant announcements are viewable
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # College Admins can view any announcement
            if self.request.user.user_type == 'college_admin':
                return queryset
            
            # Other users can view global announcements or announcements for their clubs
            q_user_specific = Q(is_global=True)
            if hasattr(self.request.user, 'joined_clubs'):
                q_user_specific |= Q(club__in=self.request.user.joined_clubs.all())
            if hasattr(self.request.user, 'managed_clubs'):
                q_user_specific |= Q(club__in=self.request.user.managed_clubs.all())
            
            return queryset.filter(q_user_specific)
        else:
            # Unauthenticated users can only view global announcements
            return queryset.filter(is_global=True)


class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

    def test_func(self):
        # Only College Admins or Club Managers can create announcements
        return self.request.user.user_type in ['college_admin', 'club_manager']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author automatically
        return super().form_valid(form)

class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcement_list')
    pk_url_kwarg = 'pk'

    def test_func(self):
        announcement = self.get_object()
        # College Admin can edit any announcement
        if self.request.user.user_type == 'college_admin':
            return True
        # Club Manager can edit their own announcements (if club-specific)
        if self.request.user.user_type == 'club_manager' and announcement.author == self.request.user:
            return True
        return False # No permission

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Pass the current user to the form
        return kwargs

class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcement_list')
    pk_url_kwarg = 'pk'

    def test_func(self):
        announcement = self.get_object()
        # College Admin can delete any announcement
        if self.request.user.user_type == 'college_admin':
            return True
        # Club Manager can delete their own announcements (if club-specific)
        if self.request.user.user_type == 'club_manager' and announcement.author == self.request.user:
            return True
        return False # No permission