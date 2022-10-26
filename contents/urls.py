# contents/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "contents"
urlpatterns = [
    path("upload/", views.FeedUload,name="feed_upload"),
    path("delete/<int:id>/", views.FeedDelete ,name="feed_delete"),
    path("update/<int:id>/", views.FeedChange, name="feed_change"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # static 경로 설정