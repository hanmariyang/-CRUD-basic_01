from django.shortcuts import render, redirect
from contents.models import Feed
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def FeedUload(request):
    if request.method == "GET":
        return render(request, "feed_upload.html")

    elif request.method == "POST":
        feed_upload = Feed()
        feed_upload.title = request.POST.get("title", '')
        feed_upload.category = request.POST.get("category", '')
        feed_upload.image = request.FILES['feed_image']
        feed_upload.content = request.POST.get("content", '')
        feed_upload.user = request.user
        feed_upload.like = 0
        feed_upload.save()
        
        return redirect('/')

@login_required
def FeedDelete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def FeedChange(request, id):
    if request.method == "GET":
        feed = Feed.objects.get(id=id)
        return render(request, 'feed_Change.html', {"feed":feed})

    if request.method == "POST":
        feed_change = Feed.objects.get(id=id)
        feed_change.title = request.POST.get('title', '')
        feed_change.category = request.POST.get('category', '')
        feed_change.image = request.FILES['feed_image']
        feed_change.content = request.POST.get('content', '')
        feed_change.save()
        
        return redirect('/')