# feedback/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Feedback, Rating

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
        }
        labels = {
            'comment': 'Your Feedback',
        }

class RatingForm(forms.ModelForm):
    # Important: Use 'rating' here to match your model field name
    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]), # Radio buttons for 1-5 score
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        label='Your Rating (1-5)'
    )

    class Meta:
        model = Rating
        fields = ['rating'] # Important: Use 'rating' here to match your model field name
