from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'username')

    

class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput, required=False, empty_value=None)

    class Meta(forms.ModelForm):
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'username')
        help_texts = {
            'username': None,
        }
    

    def clean(self):
        cleaned_data = super(CustomUserChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password's do not match"
            )
        return cleaned_data

    def save(self, request, commit=True):
        obj = super().save(commit=False)
        if self.cleaned_data['password'] is not None:
            obj.set_password(self.cleaned_data['password'])
        if commit:
            obj.save()
        else:
            return obj




        