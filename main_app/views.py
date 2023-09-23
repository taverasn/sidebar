import uuid
import boto3
import logging

from django.utils.html import format_html
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm, CommentForm, TagForm
from .models import Account, Topic, Post, Tag, Comment, AccountPhoto, TopicPhoto, PostPhoto
from django.contrib.auth.models import User

S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
BUCKET = "sidebar-new"
logger = logging.getLogger(__name__)


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
def account_dashboard(request, user_id):
    account = Account.objects.get(user_id=user_id)
    return render(request, "dashboard/account.html", {"account": account})

def dashboard_topics(request):
    topics = Topic.objects.filter(user=request.user)
    return render(request, 'dashboard/topic.html', {'topics': topics})

def dashboard_posts(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'dashboard/post.html', {'posts': posts})

def dashboard_upvoted(request):
    return render(request, 'dashboard/upvotedposts.html')

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
    tag_form = TagForm()
    return render(
        request,
        "topics/detail.html",
        {
            "topic": topic,
            "post_form": post_form,
            "tag_form": tag_form,
        },
    )


class TopicList(LoginRequiredMixin, ListView):
    model = Topic


class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TopicUpdate(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = ["title", "description"]


class TopicDelete(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = "/topics/"

# Tag Views

@login_required
def add_tag(request, topic_id):
    form = TagForm(request.POST)
    if form.is_valid():
        new_tag = form.save(commit=False)
        new_tag.topic_id = topic_id
        new_tag.save()
    return redirect("topics_detail", topic_id=topic_id)

# Post Views


@login_required
def add_post(request, user_id, topic_id):
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.topic_id = topic_id
        new_post.user_id = user_id
        new_post.save()
    return redirect("topics_detail", topic_id=topic_id)

@login_required
def post_detail(request, topic_id, post_id):
    topic = Topic.objects.get(id=topic_id)
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    return render(
        request,
        "post/detail.html",
        {"post": post, "topic": topic, "comment_form": comment_form},
    )


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "description"]


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/topics/"

# Post Vote Views


def upvote_post(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).upvotes.add(user_id)
    return redirect("topics_detail", topic_id=topic_id)


def downvote_post(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).downvotes.add(user_id)
    return redirect("topics_detail", topic_id=topic_id)


def unupvote_post(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).upvotes.remove(user_id)
    return redirect("topics_detail", topic_id=topic_id)


def undownvote_post(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).downvotes.remove(user_id)
    return redirect("topics_detail", topic_id=topic_id)

def upvote_postdetail(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).upvotes.add(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)


def downvote_postdetail(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).downvotes.add(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)


def unupvote_postdetail(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).upvotes.remove(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)


def undownvote_postdetail(request, topic_id, post_id, user_id):
    Post.objects.get(id=post_id).downvotes.remove(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)

# Comment Views


@login_required
def add_comment(request, user_id, topic_id, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user_id = user_id
        new_comment.save()
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["text"]


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = "/topics/"

# Comment Like Views

def like_comment(request, topic_id, post_id, comment_id, user_id):
    Comment.objects.get(id=comment_id).likes.add(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)

def dislike_comment(request, topic_id, post_id, comment_id, user_id):
    Comment.objects.get(id=comment_id).dislikes.add(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)

def unlike_comment(request, topic_id, post_id, comment_id, user_id):
    Comment.objects.get(id=comment_id).likes.remove(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)

def undislike_comment(request, topic_id, post_id, comment_id, user_id):
    Comment.objects.get(id=comment_id).dislikes.remove(user_id)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)

# Bookmark Views


@login_required
def bookmark_topic(request, topic_id, user_id):
    Account.objects.get(user_id=user_id).bookmarks.add(topic_id)
    return redirect("topics_detail", topic_id=topic_id)


@login_required
def unbookmark_topic(request, topic_id, user_id):
    Account.objects.get(user_id=user_id).bookmarks.remove(topic_id)
    return redirect("topics_detail", topic_id=topic_id)


# Photo Views


@login_required
def account_photo(request, user_id):
    photo_file = request.FILES.get("photo_file", None)

    if photo_file:
        s3 = boto3.client("s3")

        index_of_last_period = photo_file.name.rfind(".")

        key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)

            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = AccountPhoto(url=url, user_id=user_id)
            photo.save()
        except Exception as e:
            print("An error occurred uploading file to S3 AWS:", e)
    return redirect("account_dashboard", user_id=user_id)


@login_required
def topic_photo(request, topic_id):
    photo_file = request.FILES.get("photo_file", None)

    if photo_file:
        s3 = boto3.client("s3")

        index_of_last_period = photo_file.name.rfind(".")

        key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)

            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = TopicPhoto(url=url, topic_id=topic_id)
            photo.save()
        except Exception as e:
            print("An error occurred uploading file to S3 AWS:", e)
    return redirect("topics_detail", topic_id=topic_id)


@login_required
def post_photo(request, topic_id, post_id):
    photo_file = request.FILES.get("photo_file", None)

    if photo_file:
        s3 = boto3.client("s3")

        index_of_last_period = photo_file.name.rfind(".")

        key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)

            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = PostPhoto(url=url, post_id=post_id)
            photo.save()
        except Exception as e:
            print("An error occurred uploading file to S3 AWS:", e)
    return redirect("post_detail", topic_id=topic_id, post_id=post_id)
