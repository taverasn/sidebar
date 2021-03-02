from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Comment(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    text = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.created}"

    class Meta:
        ordering = ["created"]


class Post(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created"]


class Topic(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("topic_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-created"]


class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.last_name} {self.last_name}"


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()


class Bookmark(models.Model):
    bookmark = models.ManyToManyField(Topic)
    account = models.ManyToManyField(Account)

    def __str__(self):
        return f"{self.bookmark}"


class AccountPhoto(models.Model):
    url = models.CharField(max_length=200)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo for {self.account}"


class TopicPhoto(models.Model):
    url = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo for {self.topic}"


class PostPhoto(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo for {self.post}"