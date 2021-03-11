from django.forms import ModelForm

from .models import Post, Comment, Tag


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['text']

