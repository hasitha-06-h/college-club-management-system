from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating a new user.
    It extends Django's built-in UserCreationForm to include
    the 'user_type' and 'email' fields from our CustomUser model.
    """
    # Restrict user_type choices for initial signup
    # A regular user can only sign up as a 'student' or 'club_officer'.
    # 'college_admin' role should be assigned manually by an existing admin.
    user_type = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('club_officer', 'Club Officer'),
        ],
        label="I am a", # More user-friendly label
        help_text="Select your primary role. College Admin roles are assigned by system administrators."
    )

    class Meta(UserCreationForm.Meta):
        """
        Meta class to define the model and fields for the form.
        We inherit from UserCreationForm.Meta to get default fields,
        then add our custom fields.
        """
        model = CustomUser
        # UserCreationForm.Meta.fields typically includes 'username', 'password', 'password2'
        fields = UserCreationForm.Meta.fields + ('user_type', 'email',)

    def clean_email(self):
        """
        Custom cleaning method for the email field to ensure uniqueness.
        UserCreationForm doesn't enforce email uniqueness by default.
        """
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for changing an existing user.
    This form is typically used in the Django admin interface.
    """
    class Meta:
        """
        Meta class to define the model and fields for the form.
        We inherit from UserChangeForm.Meta to get default fields.
        """
        model = CustomUser
        # UserChangeForm.Meta.fields includes most standard user fields.
        # We don't need to explicitly add 'user_type' here if we want
        # the admin to be able to modify it directly, as it's part of
        # the standard fieldsets in UserAdmin (which CustomUserAdmin extends).
        fields = UserChangeForm.Meta.fields