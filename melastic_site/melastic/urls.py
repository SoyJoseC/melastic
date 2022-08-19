from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('admin_add_group/', views.admin_add_group, name='admin_add_group')
]