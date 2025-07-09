# clubs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg # For average rating
from .models import Club, ClubMembership
from .forms import ClubForm
from college_club_management.decorators import CollegeAdminRequiredMixin, ClubManagerRequiredMixin

class ClubListView(ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    paginate_by = 9 # Display 9 clubs per page

class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    slug_url_kwarg = 'slug' # Ensure this matches your URL pattern

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.get_object()
        
        is_member = False
        if self.request.user.is_authenticated:
            is_member = club.members.filter(id=self.request.user.id).exists()
        
        context['is_member'] = is_member
        context['members'] = club.members.all()
        # Calculate average rating
        # Note: 'ratings' is a GenericRelation, so you need the feedback_tags for template side
        context['average_rating'] = club.ratings.aggregate(Avg('rating'))['rating__avg']
        context['feedbacks'] = club.feedback.all().order_by('-created_at')
        return context

@login_required
def join_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not ClubMembership.objects.filter(user=request.user, club=club).exists():
        ClubMembership.objects.create(user=request.user, club=club)
        club.members.add(request.user) # Also add to ManyToMany field
        messages.success(request, f'You have successfully joined {club.title}!')
    else:
        messages.info(request, f'You are already a member of {club.title}.')
    return redirect('club_detail', slug=slug)

@login_required
def leave_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    membership = ClubMembership.objects.filter(user=request.user, club=club)
    if membership.exists():
        membership.delete()
        club.members.remove(request.user) # Also remove from ManyToMany field
        messages.success(request, f'You have successfully left {club.title}.')
    else:
        messages.info(request, f'You are not a member of {club.title}.')
    return redirect('club_detail', slug=slug)

# Club creation is restricted to College Admins
class ClubCreateView(LoginRequiredMixin, CollegeAdminRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('club_list')

    def form_valid(self, form):
        messages.success(self.request, f'Club "{form.instance.title}" created successfully!')
        return super().form_valid(form)

# Club update is restricted to College Admins or the assigned Club Manager
class ClubUpdateView(LoginRequiredMixin, ClubManagerRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        messages.success(self.request, f'Club "{self.object.title}" updated successfully!')
        return reverse_lazy('club_detail', kwargs={'slug': self.object.slug})

# Club deletion is restricted to College Admins
class ClubDeleteView(LoginRequiredMixin, CollegeAdminRequiredMixin, DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'
    success_url = reverse_lazy('club_list')
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, f'Club "{self.object.title}" deleted successfully!')
        return super().form_valid(form)