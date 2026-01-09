from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

class Video(models.Model):
    title = models.CharField(verbose_name="タイトル",max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/', verbose_name="動画")
    thumbnail = models.ImageField(upload_to='thumbnails/',verbose_name="サムネイル", blank=True, null=True)
    message = models.TextField(verbose_name="投稿者コメント", blank=True, default="コメントなし")
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)
    def clean(self):
        super().clean()
        if self.video_file:
            if not self.video_file.name.lower().endswith(".mp4"):
                raise ValidationError({"video_file": "動画は mp4 形式のみアップロードできます。"})

class VideoComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name="動画", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="動画へのコメント",)
    created_at = models.DateTimeField(verbose_name="コメント投稿日時", auto_now_add=True)


class Good(models.Model):
    video = models.ForeignKey(Video, verbose_name="動画", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ("video", "user")
