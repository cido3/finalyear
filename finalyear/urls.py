"""
URL configuration for finalyear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard, analytics
from django.contrib.auth import views as auth_views
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notification/read/<int:id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/delete/<int:id>/', views.delete_notification, name='delete_notification'),
    path('', dashboard, name='dashboard'),
    path('analytics/', analytics, name='analytics'),
     path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]