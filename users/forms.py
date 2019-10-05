from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'username')

    

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'username')
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=255, widget=forms.PasswordInput)

    def save(self, request, commit=True):
        if request.POST['password'] != request.POST['confirm_password']:
            raise forms.ValidationError("Password's do not match")
        else:
            obj = super().save(commit=False)
            obj.set_password(request.POST['password'])
            if commit:
                obj.save()
            else:
                return obj




        