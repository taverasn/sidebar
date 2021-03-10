from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("topics_detail", kwargs={"topic_id": self.id})

    class Meta:
        ordering = ["-created"]

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bookmarks = models.ManyToManyField(Topic)

    def __str__(self):
        return f"{self.last_name} {self.last_name}"
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    upvotes = models.ManyToManyField(Account, related_name="upvotes")
    downvotes = models.ManyToManyField(Account, related_name="downvotes")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"post_id": self.id, "topic_id": self.topic.id})

    class Meta:
        ordering = ["-created"]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    text = models.TextField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(Account, related_name="likes")
    dislikes = models.ManyToManyField(Account, related_name="dislikes")


    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"topic_id": self.post.topic.id, "post_id": self.post.id})
    

    def __str__(self):
        return f"{self.created}"

    class Meta:
        ordering = ["created"]

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()

class AccountPhoto(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo for {self.user_id} @{self.url}"

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
