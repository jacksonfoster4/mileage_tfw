from django.urls import path
from .views import SignUpView, edit

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit/', edit, name='edit')
]