# clubs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClubListView.as_view(), name='club_list'),
    path('create/', views.ClubCreateView.as_view(), name='club_create'),
    path('<slug:slug>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('<slug:slug>/join/', views.join_club, name='join_club'),
    path('<slug:slug>/leave/', views.leave_club, name='leave_club'),
    path('<slug:slug>/edit/', views.ClubUpdateView.as_view(), name='club_edit'),
    path('<slug:slug>/delete/', views.ClubDeleteView.as_view(), name='club_delete'),
]