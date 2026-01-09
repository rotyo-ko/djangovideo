from django import forms

from .models import Video, VideoComment


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "video_file", "thumbnail", "message"]
    
    
class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "コメントを書く..."
            })
        }


