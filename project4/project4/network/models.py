from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    text = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"Post {self.id} authored by {self.user} on {self.date.strftime('%d %b %Y %H %S')}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_user")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    def __str__(self):
        return f"{self.user} is following {self.followed}"

class Like(models.Model):
    user = user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user} liked {self.liked_post.user}'s post"