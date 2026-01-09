import shutil
import tempfile
from PIL import Image
from pathlib import Path
from io import BytesIO

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import CustomUser
from ..models import Video

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class VideoCreateTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@example.com",
            nickname="nickname",
            password="password1234",
        )
        self.client.login(email=self.user.email, password="password1234")
    
    def tearDown(self):
    # 一時MEDIAディレクトリをクリーンアップ
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
    
    def make_test_image(self, size=(2000, 1500), color=(255, 0, 0)):
        """メモリ上にテスト画像を生成"""
        image = Image.new("RGB", size, color)
        buf = BytesIO()
        image.save(buf, format="JPEG")
        return SimpleUploadedFile("test.jpg", buf.getvalue(), content_type="image/jpeg")
    
    def test_post_video(self):
        image = self.make_test_image()
        # 偽の動画ファイルを作成
        fake_video = SimpleUploadedFile(
            "video.mp4",
            b"\x00\x00\x00\x20ftypmp42",
            content_type="video/mp4"
        )
        res = self.client.post(reverse("videoboard:create"),
                               data={"title":"test",
                                     "video_file": fake_video,
                                     "thumbnail": image,
                                     "message": "test_message"
                                     }
                                )
        self.assertRedirects(res, reverse("videoboard:list"))
        self.assertEqual(res.status_code, 302)
        video = Video.objects.first()
        video_path = Path(video.video_file.path) # videoファイルが保存されているパス
        thumb_path = Path(video.thumbnail.path)  # thumbnailファイルが保存されているパス

        self.assertTrue(video_path.exists())
        self.assertTrue(thumb_path.exists())
        # サムネイルのサイズを確認
        with Image.open(thumb_path) as thumb:
            self.assertEqual(thumb.size, (300, 225))
        
        self.assertEqual(video.title, "test")
        self.assertEqual(video.message, "test_message")
        self.assertEqual(video.user.nickname, "nickname")
    
    def test_post_not_mp4(self):
        image = self.make_test_image()

        fake_video_avi = SimpleUploadedFile(
            "test.avi",
            b"\x00\x00\x00\x20ftypavi2",
            content_type="video/avi"
            )
        res = self.client.post(
            reverse("videoboard:create"),
            data={"title":"test",
                  "video_file": fake_video_avi,
                  "thumbnail": image,
                  "message":"test_message"
                  }, follow=True)
        # status_codeは200になる
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "videoboard/post_form.html")
        # Videoオブジェクトがないことを確認
        self.assertEqual(len(Video.objects.all()), 0)
        # バリデーションエラーメッセージの確認
        
    def test_post_without_login(self):
        # ログアウトして、postしようとする
        self.client.logout()

        image = self.make_test_image()
        fake_video = SimpleUploadedFile(
            "video.mp4",
            b"\x00\x00\x00\x20ftypmp42",
            content_type="video/mp4"
        )
        res = self.client.post(reverse("videoboard:create"),
                               data={"title":"test",
                                     "video_file": fake_video,
                                     "thumbnail": image,
                                     "message": "test_message"
                                     }
                                )
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)






