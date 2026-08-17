from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.generics import (GenericAPIView, 
    ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView)


from rest_framework.viewsets import ViewSet , ModelViewSet

from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token

from rest_framework.filters import SearchFilter, OrderingFilter

from django.shortcuts import get_object_or_404

from blog.models import (Post, Category, Tag, Comment)

from . permissions import IsAuthorOrStaff , IsStaffOrReadOnly

from . pagination import PostPagination


from .serializers import ( PostCreateSerializer,
    PostDetailSerializer,PostListSerializer,
    PostUpdateSerializer , CategoryListSerializer,
    CategoryDetailSerializer,CategoryCreateSerializer,
    CategoryUpdateSerializer, TagListSerializer,
    TagDetailSerializer, TagCreateSerializer,
    TagUpdateSerializer ,UserProfileSerializer,
    LoginSerializer ,UserRegistrationSerializer,
    ChangePasswordSerializer ,CommentSerializer
    )



# @api_view ->>>
#  It tells DRF:

# "Treat this function as an API endpoint."

# It also enables DRF features like:

# Request parsing
# Response rendering
# Method validation
# Browsable API

#  here ['GET']  means only get req is acceptable for this 
#  route other req will throw 405 


# function based view ...

# @api_view(["GET"])
# def post_list(request):

#     # post = Post.objects.first()

#     #  only single object here we are converting ....
#     # serializer = PostSerializer(post)

#     posts = Post.objects.all()

#     serializer = PostSerializer(posts, many= True)

#     #  The default behavior of ModelSerializer is to 
#     # represent relationships by their primary keys.
#     #  so in data we will see now as 
#     # for eg. author : its primary key

#     print(f"serializer ->\n {serializer}")
#     print(f"serializer.data ->\n {serializer.data}")

#     return Response(serializer.data)

#     # return Response({

#     #     "message": "Welcome to Blog API",

#     #     "status": "success"

#     # })


# ************  API views *********************

# api class based cb view using api view
# class PostList(APIView):

#     def get(self, request):

#         posts = Post.objects.all()

#         serializer = PostSerializer(
#             posts,
#             many=True
#         )

#         return Response(serializer.data)



#  ************* Generic Views ********************

#  generic view  
# class PostList(GenericAPIView):

#     queryset = Post.objects.all()

#     serializer_class = PostSerializer

#     def get(self, request):

#         posts = self.get_queryset()

#         serializer = self.get_serializer(
#             posts,
#             many=True
#         )

#         return Response(serializer.data)


#  *************  pecific Generic views..***********



# list api view  - used for get all objects of the qryset 
# class PostList(ListAPIView):

#     #  in this whenever we hit get request then the get
#     #  method we define in generics view is automatically
#     #  implemented in listapi view so we do not need 
#     #  to write our get method 

#     queryset = Post.objects.all()

#     serializer_class = PostSerializer 


#  retrieve api view - used  to get a particular obj of qryset.
# class PostDetail(RetrieveAPIView):

#     #  here internally it automatically does this 
#     # post = get_object_or_404(Post,pk=pk) by default 
#     #  look_up field is pk ..

#     queryset = Post.objects.all()

#     serializer_class = PostSerializer

#     lookup_field = "slug"



#  **************** ViewSets ***************************


# class PostViewSet(ViewSet):

#     def list(self, request):

#         posts = Post.objects.all()

#         serializer = PostSerializer(
#             posts,
#             many=True
#         )

#         return Response(serializer.data)


#  ************** ModelViewSet ******************


# POST Request
#       │
#       ▼
# serializer = PostCreateSerializer(...)
#       │
#       ▼
# serializer.is_valid()
#       │
#       ▼
# perform_create(serializer)
#       │
#       ▼
# serializer.save(...)
#       │
#       ▼
# Database


class PostViewSet(ModelViewSet):

    pagination_class = PostPagination

    filter_backends = [SearchFilter, OrderingFilter]

    #  this can be used to search posts based on 
    #  some keywords in title and text
    search_fields = ["title", "text"]

    ordering_fields = [
        "title",
        "created_date",
        "published_date",
    ]

    #  now we can do filtering like this and can be combined
    #  using &

    # GET /api/posts/?ordering=title

    # Descending order

    # Put - before the field:

    # GET /api/posts/?ordering=-title

    # GET /api/posts/?search=api

    # GET /api/posts/?category=django&search=api&ordering=-published_date

    # GET /api/posts/ -> will give now 5 post per page

    # GET /api/posts/?page=2

    # GET /api/posts/?page_size=10 per page 10 post

    # GET /api/posts/?category=django&page=2

    # GET /api/posts/?category=django&tag=restapi&search=api&ordering=-created_date&page=2&page_size=10

    #  so  we can combine like this..

    def get_queryset(self):

        print(f" kwargs ->> {self.kwargs}")

        queryset = Post.objects.all()

        #  take the category and tag slug from qry params.
        category = self.request.query_params.get("category")

        tag = self.request.query_params.get("tag")

        # if it has categeory slug then filter our qryset
        #  so that it can have those post 

        if category:
            queryset = queryset.filter(category__slug=category)

        #  if tag is also there then now filter based
        #  on tag slug ..
        if tag:
            queryset = queryset.filter(tags__slug=tag)


        return queryset

    
        
    #  override default class ..
    def get_serializer_class(self):

        if self.action == "list":
            return PostListSerializer

        elif self.action == "retrieve":
            
            return PostDetailSerializer

        elif self.action == "create":
            return PostCreateSerializer

        elif self.action in ["update", "partial_update"]:
            return PostUpdateSerializer

        return PostDetailSerializer


    def get_permissions(self):

        if self.action == "retrieve":
            permission_classes = [IsAuthenticated]

        elif self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated,IsAuthorOrStaff]

        else:
            permission_classes = []

        return [
            permission()
            for permission in permission_classes
        ]



    lookup_field = "slug"

    #  we will save author by ourself 
    #  this is hook 
    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user)

    


class CategoryViewSet(ModelViewSet):

    def get_queryset(self):

        return Category.objects.all()

    def get_serializer_class(self):

        if self.action == "list":
            return CategoryListSerializer

        elif self.action == "retrieve":
            return CategoryDetailSerializer

        elif self.action == "create":
            return CategoryCreateSerializer

        elif self.action in ["update", "partial_update"]:
            return CategoryUpdateSerializer

        return CategoryDetailSerializer


    lookup_field = "slug"

    permission_classes = [IsStaffOrReadOnly]


class TagViewSet(ModelViewSet):

    def get_queryset(self):
        return Tag.objects.all()

    def get_serializer_class(self):

        if self.action == "list":
            return TagListSerializer

        elif self.action == "retrieve":
            return TagDetailSerializer

        elif self.action == "create":
            return TagCreateSerializer

        elif self.action in ["update", "partial_update"]:
            return TagUpdateSerializer

        return TagDetailSerializer

    lookup_field = "slug"

    permission_classes = [IsStaffOrReadOnly]



class RegistrationView(APIView):

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        print(f"serializer-> {serializer}")

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                }
            },
            status=status.HTTP_201_CREATED
        )




class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        print(f"serializer-initial data -> {serializer.initial_data}")

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(
            user=user
        )

        print(f"token -> {token}")  
        print(f"created -> {created}")  

        return Response(
            {
                "token": token.key
            },
            status=status.HTTP_200_OK
        )

    


class UserProfileView(RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer

    permission_classes = [IsAuthenticated]
  

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = request.user

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )



class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        Token.objects.filter(
            user=request.user
        ).delete()

        return Response(
            {
                "message": f"Logged out {request.user.username} successfully."
            },
            status=status.HTTP_200_OK
        )



class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    #  kwargs is the arguments we give in url like this
    #  suppose our url is posts/post_slug/comment

    #  then our kwargs post_slug will give its value
    def get_queryset(self):

        if "post_slug" in self.kwargs :
            post = get_object_or_404(
                Post,
                slug=self.kwargs["post_slug"]
            )

            #  here we are displaying only top level 
            #  comment becoz inside comments we alreaddy
            #  displaying thier replies so no 
            #  need to display replies separately..
            return Comment.objects.filter(
                post=post, parent = None
            )

        return Comment.objects.all() 

    

    def get_serializer_context(self):

        #  first get the old context which drf provide 
        #  by its own then add our own data in it..
        context = super().get_serializer_context()

        #  add post only if it is creating comment or reply
        if "post_slug" in self.kwargs : 

            context["post"] = get_object_or_404(
                Post,
                slug=self.kwargs["post_slug"]
            )

            print(f"context -> {context}")


        return context


    def perform_create(self, serializer):

        post = get_object_or_404(
            Post,
            slug=self.kwargs["post_slug"]
        )

        serializer.save(
            post=post,
            author=self.request.user
        )


    def get_permissions(self):

        if self.action in ["list", "retrieve","create"]:
            permission_classes = [IsAuthenticated]

       
        elif self.action in [
            "update",
            "partial_update",
            "destroy"
        ]:
            permission_classes = [
                IsAuthenticated,
                IsAuthorOrStaff
            ]

        else:
            permission_classes = []

        return [
            permission()
            for permission in permission_classes
        ]

