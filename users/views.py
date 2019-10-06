from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, SetPasswordFormNoHelpText
from django.contrib.auth.views import PasswordResetConfirmView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:index')
    template_name = 'signup.html'

    def form_valid(self, form):  
        valid = super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid

@login_required
def edit(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save(request.POST)
            login(request, user)
            return render(request, 'users/users_update_form.html', { 'form': form, 'user': user, 'messages': ['Successfully updated!'] })
        else:
            return render(request, 'users/users_update_form.html', {'form': form, 'user': user})

    else:
        form = CustomUserChangeForm(instance=user)
        return render(request, 'users/users_update_form.html', {'form': form, 'user': user})


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    form_class = SetPasswordFormNoHelpText