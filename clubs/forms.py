# clubs/forms.py
from django import forms
from .models import Club
from accounts.models import CustomUser

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['title', 'description', 'photo', 'manager']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'photo': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter manager choices to only show CustomUser instances with user_type='club_officer'
        self.fields['manager'].queryset = CustomUser.objects.filter(user_type='club_officer')
        self.fields['manager'].required = False # Manager can be set later