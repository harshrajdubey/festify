from django.shortcuts import render

def home(request):
    """Landing page for Festify - accessible without authentication"""
    return render(request, 'festify/home.html')