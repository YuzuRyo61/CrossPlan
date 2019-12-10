import markdown
from gfm import AutolinkExtension

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django import forms

from fediverse.models import Post, User

def convertMarkdown(body):
    return markdown.markdown(
        body,
        extensions=[
            AutolinkExtension()
        ]
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", )

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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('display_name', 'description', 'is_bot')

    def clean_description(self):
        description = convertMarkdown(self.cleaned_data['description'])
        return description

class EditPrivacyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_manualFollow', )

class Settings_PasswordChangeForm(PasswordChangeForm):
    pass
