
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("follow_unfollow/<int:user_id>/<int:followed_id>/", views.follow_unfollow, name="follow_unfollow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path('like-count/<int:post_id>', views.get_like_count, name='like_count'),
    path("like/<int:post_id>", views.like, name="like")
]
