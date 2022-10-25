# basic_01/views.py
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'home.html')
        else:
            return redirect('login')