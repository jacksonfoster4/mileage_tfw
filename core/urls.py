from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('list/', views.list, name='list'),
    path('<int:id>/edit', views.edit, name="edit"),
    path('<int:id>/detail', views.detail, name="detail"),
    path('<int:id>/delete', views.delete, name='delete')
]