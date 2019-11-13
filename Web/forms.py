import markdown

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django import forms

from fediverse.models import Post, User

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
        description = self.cleaned_data['description']
        description = markdown.Markdown().convert(description)
        return description

class EditPrivacyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_manualFollow', )

class Settings_PasswordChangeForm(PasswordChangeForm):
    pass
