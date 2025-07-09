



# events/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # For views that require login
from django.utils import timezone # For filtering by date
from .models import Event
from .forms import EventForm # You'll create this form next
from college_club_management.decorators import CollegeAdminRequiredMixin, ClubManagerRequiredMixin # Assuming these are defined

class EventCalendarView(ListView):
    model = Event
    template_name = 'events/event_calendar.html'
    context_object_name = 'events'
    paginate_by = 10 # Display 10 events per page

    def get_queryset(self):
        # By default, show only upcoming events, ordered by date and time
        queryset = super().get_queryset().filter(
            date__gte=timezone.localdate() # Filter for events today or in the future
        ).order_by('date', 'time')

        # Optional: Add filtering by club or search (example)
        club_slug = self.request.GET.get('club')
        if club_slug:
            queryset = queryset.filter(club__slug=club_slug)
        
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) # Simple title search
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from clubs.models import Club
        context['clubs'] = Club.objects.all()
        context['selected_club'] = self.request.GET.get('club', '')
        return context

# Optional: Detail view for a single event
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'pk' # Expects primary key in URL

# Optional: Create/Update/Delete views (requires forms.py)
class EventCreateView(LoginRequiredMixin, ClubManagerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_calendar') # Redirect after successful creation

    def form_valid(self, form):
        form.instance.created_by = self.request.user # Set the creator
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, ClubManagerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_calendar')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only managers of the specific club or college admins can edit
        if self.request.user.user_type == 'college_admin':
            return queryset
        return queryset.filter(created_by=self.request.user) # Or filter by club.manager for a specific club's event

class EventDeleteView(LoginRequiredMixin, CollegeAdminRequiredMixin, DeleteView): # Only CollegeAdmin can delete globally
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_calendar')