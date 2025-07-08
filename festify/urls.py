from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Landing page at root
    path('', include('users.urls')),    # Include user URLs
]
