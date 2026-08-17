from django.urls import path
from rest_framework.routers import DefaultRouter


from . import views


# urlpatterns = [

#     # path(
#     #     "posts/",
#     #     views.PostList.as_view(),
#     #     name="api_post_list"
#     # ),

#     # path(
#     #     "posts/<slug:slug>/",
#     #     views.PostDetail.as_view(),
#     # )

#     #  path(
#     #     "posts/",
#     #     views.PostViewSet.as_view(
#     #         {
#     #             "get": "list",
#     #         }
#     #     ),
#     #     name="api_post_list",
#     # ),
# ]



router = DefaultRouter()

#  here base name generates names of our urls like 
#  this ->>> posts-list,  posts-detail

router.register(
    "posts",
    views.PostViewSet,
    basename="posts"
)

router.register(
    "categories",
    views.CategoryViewSet,
    basename="category",
)

router.register(
    "tags",
    views.TagViewSet,
    basename="tag"
)

# Internally, the router generated something similar to:

# GET      /api/posts/
# POST     /api/posts/

# GET      /api/posts/<pk>/
# PUT      /api/posts/<pk>/
# PATCH    /api/posts/<pk>/
# DELETE   /api/posts/<pk>/


urlpatterns = router.urls


urlpatterns += [

    path(
        "register/",
        views.RegistrationView.as_view(),
        name="register"
    ),

    path(
        "login/",
        views.LoginView.as_view(),
        name="login"
    ),

    path("profile/", 
         views.UserProfileView.as_view(), 
         name="user-profile"),

    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password"
    ),

    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout"
    ),

    path(
        "posts/<slug:post_slug>/comments/",
        views.CommentViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="post-comments",
    ),

    path(
        "comments/<int:pk>/",
        views.CommentViewSet.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "put": "update",
            "delete": "destroy",
        }),
        name="comment-detail",
    ),

]

