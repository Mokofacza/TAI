# forms.py w Twojej aplikacji Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Komentarz
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Tytuł',
            'content': 'Treść',
            'image': 'Obraz',
        }

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class KomentarzForm(forms.ModelForm):
    blogpost_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Komentarz
        fields = ['tresc', 'blogpost_id']

    def __init__(self, *args, **kwargs):
        super(KomentarzForm, self).__init__(*args, **kwargs)
        self.fields['blogpost_id'].required = False
        self.fields['tresc'].widget.attrs.update({'class': 'form-control'})
