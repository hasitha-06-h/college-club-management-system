# events/forms.py
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'club']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Get the current user from view
        super().__init__(*args, **kwargs)
        # If the user is a club manager, limit the club choices to clubs they manage
        if user and user.user_type == 'club_manager':
            self.fields['club'].queryset = user.managed_clubs.all()
        # If the user is a normal student, they shouldn't create events directly linked to a club (unless allowed)
        # If user is admin, they see all clubs.