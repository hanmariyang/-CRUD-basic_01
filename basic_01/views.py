# basic_01/views.py
from django.shortcuts import render, redirect
from contents.models import Feed, Comment

def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            feeds_all = Feed.objects.all().order_by('-created_at')
            feeds = []
            for feed in feeds_all:
                comment = Comment.objects.filter(feed_id=feed.id)
                feed.comment = comment
                feeds.append(feed)

            return render(request, 'home.html', { 'feeds' : feeds })
        else:
            return redirect('accounts/checkin/')