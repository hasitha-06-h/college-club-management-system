# announcements/forms.py
from django import forms
from .models import Announcement
from clubs.models import Club # Needed for queryset filtering

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_global', 'club']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your announcement here...'}),
        }
        labels = {
            'is_global': 'Global Announcement',
            'club': 'Target Club (Leave blank for Global)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Get the current user from the view
        super().__init__(*args, **kwargs)

        # Ensure that 'author' field is not shown in form as it's set automatically
        # You might also remove it from 'fields' list above if you don't want it editable
        if 'author' in self.fields:
            self.fields['author'].widget = forms.HiddenInput() # Hide author field if passed

        # Adjust 'club' field based on user type
        if user:
            if user.user_type == 'club_manager':
                # Managers can only post announcements for clubs they manage
                self.fields['club'].queryset = Club.objects.filter(manager=user)
                self.fields['is_global'].widget = forms.HiddenInput() # Managers cannot create global announcements
                self.fields['is_global'].initial = False # Default to non-global for managers
            elif user.user_type == 'college_admin':
                # Admins can post for any club or global
                self.fields['club'].queryset = Club.objects.all()
            else:
                # Other users (students) cannot create announcements via this form
                # This form should only be accessible via permissions in views
                pass
        
        # Add JavaScript to dynamically show/hide the club field based on 'is_global' checkbox
        self.fields['is_global'].widget.attrs['onchange'] = 'toggleClubField(this)'
        if self.instance and self.instance.is_global:
            self.fields['club'].widget.attrs['style'] = 'display: none;'
        elif not self.instance.is_global and not self.instance.club:
             self.fields['club'].required = True # Make club required if not global and no instance


    def clean(self):
        cleaned_data = super().clean()
        is_global = cleaned_data.get('is_global')
        club = cleaned_data.get('club')

        if is_global and club:
            raise forms.ValidationError(
                "A global announcement cannot be assigned to a specific club. Please uncheck 'Global Announcement' or remove the club selection."
            )
        if not is_global and not club:
            raise forms.ValidationError(
                "A club-specific announcement must have a club selected. Please select a club or check 'Global Announcement'."
            )
        return cleaned_data