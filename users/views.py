from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

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
def edit(request, id):
    if request.method == 'POST':
        pass
    else:
        pass


