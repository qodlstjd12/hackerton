from django import forms
from .models import Post1

class PostForm(forms.ModelForm):
    class Meta:
        model = Post1
        fields = ['title', 'body']



class RecoveryPwForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput,)

    class Meta:
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })

from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

