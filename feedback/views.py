from django.shortcuts import render

# Create your views here.
# feedback/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Avg

from django.contrib.contenttypes.models import ContentType
from .models import Feedback, Rating
from .forms import FeedbackForm, RatingForm

# Helper function to get content_object from slug/PK and model name
def get_content_object(model_name, identifier):
    try:
        model_class = ContentType.objects.get(model=model_name).model_class()
    except ContentType.DoesNotExist:
        return None # Model not found in ContentTypes

    if not model_class:
        return None # Should not happen if ContentType exists but just a safety

    try:
        # Check if the model has a slug field and identifier is not purely numeric
        if hasattr(model_class, 'slug') and not str(identifier).isdigit():
            obj = model_class.objects.get(slug=identifier)
        else: # Otherwise, assume it's a primary key
            obj = model_class.objects.get(pk=identifier)
    except model_class.DoesNotExist:
        return None
    except ValueError: # Catch if PK conversion fails for non-digit identifier
        return None
    return obj


class SubmitFeedbackView(LoginRequiredMixin, View):
    template_name = 'feedback/feedback_form.html'

    def get(self, request, model_name, identifier):
        content_object = get_content_object(model_name, identifier)
        if not content_object:
            messages.error(request, "Object not found for feedback.")
            return redirect('home') # Redirect to your home page or an error page

        feedback_form = FeedbackForm()
        rating_form = RatingForm()
        context = {
            'feedback_form': feedback_form,
            'rating_form': rating_form,
            'content_object': content_object,
            'model_name': model_name,
            'identifier': identifier,
        }
        return render(request, self.template_name, context)

    def post(self, request, model_name, identifier):
        content_object = get_content_object(model_name, identifier)
        if not content_object:
            messages.error(request, "Object not found for feedback submission.")
            return redirect('home')

        content_type = ContentType.objects.get_for_model(content_object)

        feedback_form = FeedbackForm(request.POST)
        rating_form = RatingForm(request.POST)

        if 'submit_feedback' in request.POST: # Check which form button was clicked
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.content_type = content_type
                feedback.object_id = content_object.id
                feedback.save()
                messages.success(request, "Your feedback has been submitted!")
                # Redirect back to the object's detail page (assuming it has get_absolute_url)
                return redirect(content_object.get_absolute_url())
            else:
                messages.error(request, "There was an error submitting your feedback. Please correct the errors.")

        elif 'submit_rating' in request.POST: # Check which form button was clicked
            if rating_form.is_valid():
                # Check if user has already rated this object
                existing_rating = Rating.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=content_object.id
                ).first()

                if existing_rating:
                    messages.warning(request, "You have already rated this item. Your previous rating has been updated.")
                    existing_rating.rating = rating_form.cleaned_data['rating'] # Use 'rating' here
                    existing_rating.save()
                else:
                    rating = rating_form.save(commit=False)
                    rating.user = request.user
                    rating.content_type = content_type
                    rating.object_id = content_object.id
                    rating.save()
                    messages.success(request, "Your rating has been submitted!")
                return redirect(content_object.get_absolute_url())
            else:
                messages.error(request, "There was an error submitting your rating. Please correct the errors.")

        # Re-render the form if there were errors or if no specific button was pressed (shouldn't happen)
        context = {
            'feedback_form': feedback_form,
            'rating_form': rating_form,
            'content_object': content_object,
            'model_name': model_name,
            'identifier': identifier,
        }
        return render(request, self.template_name, context)

# View to display all feedback/ratings for an object
class ObjectFeedbackListView(View):
    template_name = 'feedback/object_feedback_list.html'

    def get(self, request, model_name, identifier):
        content_object = get_content_object(model_name, identifier)
        if not content_object:
            messages.error(request, "Object not found for feedback list.")
            return redirect('home')

        feedbacks = Feedback.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.id
        )
        ratings = Rating.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.id
        )

        # Calculate average rating
        # Use 'rating' here
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

        context = {
            'content_object': content_object,
            'feedbacks': feedbacks,
            'ratings': ratings,
            'average_rating': average_rating,
            'model_name': model_name, # Pass model_name for template logic
            'identifier': identifier, # Pass identifier for template logic
        }
        return render(request, self.template_name, context)

# Optional: API endpoint for average rating (e.g., for AJAX)
def get_average_rating_api(request, model_name, identifier):
    content_object = get_content_object(model_name, identifier)
    if not content_object:
        return JsonResponse({'error': 'Object not found'}, status=404)

    # Use 'rating' here
    average_rating = content_object.ratings.aggregate(Avg('rating'))['rating__avg']
    return JsonResponse({'average_rating': average_rating or 0})