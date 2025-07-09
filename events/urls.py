# events/urls.py

# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventCalendarView.as_view(), name='event_calendar'), # The main calendar page
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]