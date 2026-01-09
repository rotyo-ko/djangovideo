from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=50, label="ニックネーム", required=False)

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data["nickname"]
        user.save()
        return user
