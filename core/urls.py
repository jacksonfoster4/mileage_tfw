from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('list/', views.list, name='list'),
    path('<int:id>', views.detail, name="detail"),
    path('<int:id>/edit', views.edit, name="edit"),
    path('<int:id>/delete', views.delete, name='delete'),
    path('<int:id>/sheet', views.view_sheet, name='sheet')
]