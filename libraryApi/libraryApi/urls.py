"""
URL configuration for libraryApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from bookReplacement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculate_cost/', views.calculate_total_cost),
    path('book/', views.create_book, name='create_book'),
    path('student/', views.create_student, name='create_student'),
    path('request/', views.create_request, name='create_request'),
    path('books/', views.get_books, name='get_books'),
    path('students/', views.get_students, name='get_students'),
    path('requests/', views.get_requests, name='get_requests'),


]
