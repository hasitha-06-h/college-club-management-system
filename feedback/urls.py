
# feedback/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/<str:model_name>/<str:identifier>/', views.SubmitFeedbackView.as_view(), name='submit_feedback'),
    path('list/<str:model_name>/<str:identifier>/', views.ObjectFeedbackListView.as_view(), name='object_feedback_list'),
    path('api/avg_rating/<str:model_name>/<str:identifier>/', views.get_average_rating_api, name='api_avg_rating'),
]