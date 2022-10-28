from django.shortcuts import render, redirect
from contents.models import Feed, Comment
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
    if feed.user == request.user:
        feed.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])

@login_required
def FeedChange(request, id):
    if request.method == "GET":
        feed = Feed.objects.get(id=id)
        if feed.user == request.user:
            return render(request, 'feed_Change.html', {"feed":feed})
        else:
            return redirect(request.META['HTTP_REFERER'])

    if request.method == "POST":
        feed_change = Feed.objects.get(id=id)
        feed_change.title = request.POST.get('title', '')
        feed_change.category = request.POST.get('category', '')
        feed_change.image = request.FILES['feed_image']
        feed_change.content = request.POST.get('content', '')
        feed_change.save()
        
        return redirect('/')


@login_required
def likes(request, id):
    if request.method == 'POST':
        feed = Feed.objects.get(id=id)
        if feed.like_authors.filter(id=request.user.id).exists():
            feed.like_authors.remove(request.user)
        else:
            feed.like_authors.add(request.user)

        return redirect(request.META['HTTP_REFERER'])
        



def write_comment(request, id): 
    if request.method == 'POST':
        current_comment = Feed.objects.get(id=id)
        comment = request.POST.get('comment')

        FC = Comment()
        FC.comment = comment
        FC.user = request.user
        FC.feed = current_comment
        FC.save()

    return redirect(request.META['HTTP_REFERER'])


def delete_comment(request, id): 
        comment = Comment.objects.get(id=id)        
        if comment.user == request.user:
            comment.delete()
            return redirect('/')
        else:
            return redirect('/')
        
        
