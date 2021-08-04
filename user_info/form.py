from django import forms

def save(self, commit=True):
    user = super(CsRegisterForm, self).save(commit=False)
    user.is_active = False
    user.save()

from .models import Post1

class PostForm(forms.ModelForm):
    class Meta:
        model = Post1
        fields = ['title', 'body']

