from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo_list import views as todo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', todo_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='todo_list/login.html'), name='login'),
    path('logout/', todo_views.logout_view, name='logout'),
    path('', include('todo_list.urls')),  # Keep this as the last path to catch all other URLs
]