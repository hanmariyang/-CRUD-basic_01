from django.db import models
from accounts.models import UserModel


# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    image = models.ImageField(default="", upload_to="feed_images/")
    content = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    like_authors = models.ManyToManyField(UserModel, related_name='like_feeds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)


class Comment(models.Model):

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)