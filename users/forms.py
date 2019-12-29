from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


# Authentication

ERROR_MESSAGE = 'Your email and password combination was not valid'
ERROR_MESSAGE_RESTRICTED = 'You do not have the required permissions'
ERROR_MESSAGE_INACTIVE = 'Your account is not active'

UserModel = get_user_model()


class EmailUserCreationForm(forms.ModelForm):
    """Override the default UserCreationForm to force email-as-username
    behavior."""

    email = forms.EmailField(label='Email', max_length=75)

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already ' 'exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(None)
        if commit:
            user.save()
        return user


class EmailUserChangeForm(UserChangeForm):
    """Override the default UserChangeForm to force email-as-username
    behavior."""

    email = forms.EmailField(label='Email', max_length=75)

    class Meta:
        model = UserModel
        fields = ('email',)
