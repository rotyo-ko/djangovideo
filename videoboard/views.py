from PIL import Image
from pathlib import Path

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.conf import settings

from .models import Video, VideoComment, Good
from .forms import VideoCommentForm

class VideoListView(ListView):
    model = Video
    template_name = "videoboard/list.html"
    paginate_by = 9
    def get_queryset(self):
        videos = Video.objects.order_by("-created_at")
        return videos


class VideoMyListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = "videoboard/myvideo.html"
    paginate_by = 9
    def get_queryset(self):
        videos = Video.objects.filter(user=self.request.user)
        return videos


class VideoDetailView(DetailView):
    model = Video
    template_name = "videoboard/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = VideoComment.objects.filter(video=self.object)
        video = self.object
        good_count = Good.objects.filter(video=video).count()
        context["user_has_liked"] = Good.objects.filter(video=video, user=self.request.user).exists()
        context["comments"] = comments
        context["form"] = VideoCommentForm()
        context["good_count"] = good_count
        return context

def good(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == "POST":
        good = Good.objects.filter(user=request.user, video=video).first()
        if good:
            good.delete()
        else:
            Good.objects.create(user=request.user, video=video)
        return redirect("videoboard:detail", pk=video.pk)
    else:
        return redirect("videoboard:list")


class VideoCreateView(LoginRequiredMixin,CreateView):
    model = Video
    template_name = "videoboard/post_form.html"
    fields = ["title", "video_file", "thumbnail", "message"]
    success_url = reverse_lazy("videoboard:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        video = self.object 
        # form_valid()内ではsels.objectが使える。GETやPOST(form_valid()の前)ではself.objectは使えない。
        # self.get_object()はUpdate, Detailで使う
        original_thumb_path = Path(video.thumbnail.path)
        img = Image.open(original_thumb_path)
        
        thumb_size = (300, 300)
        img.thumbnail(thumb_size)

        thumb_dir = Path(settings.MEDIA_ROOT) / "thumbnails"
        thumb_name = f"thumb_{original_thumb_path.stem}.jpg"
        thumb_path = thumb_dir / thumb_name

        img.save(thumb_path, quality=85)
        video.thumbnail.name = f"thumbnails/{thumb_name}"
        video.save()

        return response
    

class VideoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """コメントだけを編集できるようにする"""
    model = Video
    template_name = "videoboard/post_form.html"
    fields = ["message"]
    
    def test_func(self):
        video = self.get_object() # Editではself.get_object()を使う
        return video.user == self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        video = self.object 
        if not video.message.strip().startswith("(修正済み)"):
            video.message = "(修正済み)" + video.message
        video.save()
        return response
    

class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = "videoboard/delete_confirm.html"
    success_url = reverse_lazy("videoboard:list")

    def test_func(self):
        video = self.get_object()
        return video.user == self.request.user
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = VideoComment
    template_name = "detail.html"
    fields = ["comment"]
    def form_valid(self, form):
        form.instance.user = self.request.user
        video = get_object_or_404(Video, pk=self.kwargs["pk"])
        form.instance.video = video
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("videoboard:detail", pk=self.kwargs["pk"])
    

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoComment
    template_name = "comment_edit.html"
    fields = ["comment"]
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        comment = self.object
        if not comment.comment.strip().startswith("(修正済み)"):
            comment.comment = "(修正済み)" + comment.comment
        comment.save()
        return response
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse("board:detail", kwargs={"pk": comment.video.pk})
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoComment
    template_name = "delete_confirm.html"
    
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse("board:detail", kwargs={"pk": comment.photo.pk})
