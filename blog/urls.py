from django.urls import path
from . import views

urlpatterns = [
    # Blog
    path("", views.post_list, name="post_list"),

    path("post/new/", views.post_new, name="post_new"),

    path("post/<slug:slug>/", views.post_detail, name="post_detail"),

    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),

    path(
    "post/<slug:slug>/counter/",
    views.increase_counter,
    name="increase_counter"
    ),

    path(
        "category/<slug:slug>/",
        views.category_posts,
        name="category_posts"
    ),
    path(
        "tag/<slug:slug>/",
        views.tag_posts,
        name="tag_posts"
    ),

    path(
        "post/<slug:slug>/comment/",
        views.add_comment,
        name="add_comment"
    ),
    
    path(
        "post/<slug:slug>/comment/<int:comment_id>/reply/",
        views.add_reply,
        name="add_reply"
    ),

    # Authentication
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),

    # Profile
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),


    path(
        "post/<slug:slug>/like/",
        views.toggle_like,
        name="toggle_like"
    ),
]