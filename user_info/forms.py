from django import forms
from .models import Post1

class PostForm(forms.ModelForm):
    class Meta:
        model = Post1
        fields = ['title', 'body']

class RecoveryIdForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput,
    )
    class Meta:
        fields = ['phone']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['phone'].label = '휴대전화번호'
        self.fields['phone'].widget.attrs.update({
            # 'placeholder': '이름을 입력해주세요',
            'class': 'form-control',
            'id': 'form_phone',
        })

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

