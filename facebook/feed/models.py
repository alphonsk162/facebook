from django.db import models
from django.contrib.auth.models import User
from user.models import UserDetails

# Create your models here.


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["from_user", "to_user"]


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User, related_name="friendships1", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="friendships2", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user1", "user2"]


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    user_profile = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    reply_to = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
