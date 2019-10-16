from django.contrib.auth.forms import AuthenticationForm
from django import forms

from fediverse.models import Post

class LoginForm(AuthenticationForm):
    pass

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
    
    def clean_body(self):
        body = self.cleaned_data['body']
        if body == None or len(body.strip()) <= 0:
            raise forms.ValidationError("投稿を空にすることはできません。")
        return body
