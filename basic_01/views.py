# basic_01/views.py
from django.shortcuts import render, redirect
from contents.models import Feed

def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            feed = Feed.objects.all().order_by('-created_at')
            print(feed)
            return render(request, 'home.html', { 'feeds' : feed })
        else:
            return redirect('accounts/checkin/')