import uuid
import boto3
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm, CommentForm
from .models import Account, Topic, Post, Comment  # ,Photo, Bookmark
from django.contrib.auth.models import User

S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
BUCKET = "sidebar-aws"


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/dashboard/accounts/create")
        else:
            error_message = "Invalid sign up - try again"

    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


def home(request):
    return render(request, "home.html")


# Account Views


@login_required
def dashboard_index(request):
    return render(request, "dashboard/index.html")


@login_required
def account_dashboard(request):
    return render(request, "dashboard/account.html")


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ["first_name", "last_name", "email", "bio"]
    success_url = "/topics/"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ["first_name", "last_name", "email", "bio"]
    success_url = "/dashboard/"


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = "/"


# Topic Views


# @login_required
# def topics_index(request):
#     return render(request, "topics/index.html")


@login_required
def topics_detail(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    post_form = PostForm()
    return render(
        request,
        "topics/detail.html",
        {
            "topic": topic,
            "post_form": post_form,
        },
    )


class TopicList(LoginRequiredMixin, ListView):
    model = Topic


class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ["title", "description"]


class TopicUpdate(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = ["title", "description"]


class TopicDelete(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = "/topics/"


# Post Views


@login_required
def add_post(request, topic_id):
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.topic_id = topic_id
        new_post.save()
    return redirect("topics_detail", topic_id=topic_id)


def post_detail(request, topic_id, post_id):
    topic = Topic.objects.get(id=topic_id)
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    return render(request, "post/detail.html", {"post": post, "topic": topic, "comment_form": comment_form})


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "description"]


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/topics/"



# Comment Views


@login_required
def add_comment(request, topic_id, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.save()
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['text']


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = "/topics/"


# Bookmark Views

# @login_required
# def bookmark_topic(request, topic_id, user_id, bookmark_id):
#     Topic.objects.get(id=topic_id).bookmarks.add(bookmark_id)
#     User.objects.get(id=user_id).bookmarks.add(bookmark_id)
#     return redirect('topic_detail', topic_id=topic_id)

# @login_required
# def unbookmark_topic(request, topic_id, user_id, bookmark_id):
#     Topic.objects.get(id=topic_id).bookmarks.delete(bookmark_id)
#     User.objects.get(id=user_id).bookmarks.delete(bookmark_id)
#     return redirect('topic_detail', topic_id=topic_id)


# Photo Views

# @login_required
# def account_photo(request, user_id):
#     photo_file = request.FILES.get('photo_file', None)

#     if photo_file:
#         s3 = boto3.client('s3')

#         index_of_last_period = photo_file.name.rfind('.')

#         key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)

#             url = f"{S3_BASE_URL}{BUCKET}/{key}"

#             photo = Photo(url=url, user_id=user_id)
#             photo.save()
#         except: print('An error occured uploading file to S3 AWS')
#     return redirect('account_dashboard', user_id=user_id)

# @login_required
# def topic_photo(request, topic_id):
#     photo_file = request.FILES.get('photo_file', None)

#     if photo_file:
#         s3 = boto3.client('s3')

#         index_of_last_period = photo_file.name.rfind('.')

#         key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)

#             url = f"{S3_BASE_URL}{BUCKET}/{key}"

#             photo = Photo(url=url, topic_id=topic_id)
#             photo.save()
#         except: print('An error occured uploading file to S3 AWS')
#     return redirect('topics_detail', topic_id=topic_id)

# @login_required
# def post_photo(request, topic_id, post_id):
#     photo_file = request.FILES.get('photo_file', None)

#     if photo_file:
#         s3 = boto3.client('s3')

#         index_of_last_period = photo_file.name.rfind('.')

#         key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)

#             url = f"{S3_BASE_URL}{BUCKET}/{key}"

#             photo = Photo(url=url, topic_id=topic_id, post_id=post_id)
#             photo.save()
#         except: print('An error occured uploading file to S3 AWS')
#     return redirect('post_detail', topic_id=topic_id, post_id=post_id)
