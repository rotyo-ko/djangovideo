from django.urls import path

from . import views

app_name = "videoboard"
urlpatterns = [
     path("", views.VideoListView.as_view(), name="list"),
     path("myvideo/", views.VideoMyListView.as_view(), name="myvideo"),
     path("videos/<int:pk>/detail/", views.VideoDetailView.as_view(),
          name="detail"),
     path("videos/create/", views.VideoCreateView.as_view(),
          name="create"),
     path("videos/<int:pk>/edit/", views.VideoEditView.as_view(),
          name="edit"),
     path("videos/<int:pk>/delete/",views.VideoDeleteView.as_view(),
          name="delete"),
     path("videos/<int:pk>/comment/",views.CommentCreateView.as_view(),
          name="comment"),
     path("comment/<int:pk>/edit/", views.CommentEditView.as_view(),
          name="comment_edit"),
     path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(),
          name="comment_delete"),
     path("videos/<int:video_id>/good/", views.good,
          name="good")
    
]