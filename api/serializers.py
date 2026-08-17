from rest_framework import serializers

from django.contrib.auth import authenticate


from blog import models 


#  modalserializer makes serializer fields, validations and
# other default methods  for us
#  automaticly so we not need to make these 

#  use serializerr when we do not have django model
# like for our login api , change pswd api etc ...




class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Category

        fields = [
            "id",
            "name",
            "slug",
        ]


#  this is used to show a particular category
#  we can later add our own fields which we wants 
#  to show in category details ...
class CategoryDetailSerializer(CategoryListSerializer):
    pass


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Category

        fields = [
            "name",
        ]


class CategoryUpdateSerializer(CategoryCreateSerializer):
    pass



class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = [
            "id",
            "name",
            "slug",
        ]


class TagDetailSerializer(TagListSerializer):
    pass


class TagCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = [
            "name",
        ]


class TagUpdateSerializer(TagCreateSerializer):
    pass





# class PostSerializer(serializers.ModelSerializer):

#     class Meta:

#         model = Post

#         fields = "__all__"




#  this is used to view the all posts..
class PostListSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only = True ,
        slug_field="username"
    )

    category = CategoryDetailSerializer(read_only=True)

    tags = TagDetailSerializer(
        many=True,
        read_only=True
    )


    class Meta:

        model = models.Post

        fields = [
            "id",
            "author" ,
            "slug",
            "title",
            "featured_image",
            "published_date",
            "text",
            "category",
            "tags",
        ]


#  this is to view the particular  post ..

class PostDetailSerializer(serializers.ModelSerializer):


    author = serializers.SlugRelatedField(
        read_only = True ,
        slug_field="username"
    )

    category = CategoryDetailSerializer(read_only=True)

    tags = TagDetailSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = models.Post


        fields = [
            "id",
            "slug",
            "title",
            "text",
            "author",
            "featured_image",
            "thumbnail",
            "category",
            "tags",
            "published_date",
            "created_date",
            "like_counter",
        ]

        #  here we actually donot need this 
        #  becoz we have already separte serializer 
        #  for read and write o/ps.
        read_only_fields = [
            "id",
            "created_date",
            "like_counter",
        ]


#  this is used to create the post .
class PostCreateSerializer(serializers.ModelSerializer):

    #  now we can give category and tags using thier names..
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field="name"
    )

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=models.Tag.objects.all(),
        slug_field="name"
    )

    class Meta:

        model = models.Post

        fields = [
            "title",
            "text",
            "category",
            "tags",
            "thumbnail",
            "featured_image",
        ]



#  used to update the post 
class PostUpdateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field="name"
    )

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=models.Tag.objects.all(),
        slug_field="name"
    )

    class Meta:

        model = models.Post

        fields = [
            "title",
            "text",
            "category",
            "tags",
            "thumbnail",
            "featured_image",
        ]



class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User

        fields = [
            "username",
            "email",
            "password",
            "city",
            "state",
            "phone_no",
            "profile_image",
            "first_name",
            "last_name",
        ]

        #  add customiztiom to our pswd field 
        #  it must be given by user when creating
        #  but not included in response ...
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    #  custome create becoz default create method
    #  does not hash pswd ...
    def create(self, validated_data):

        #  validate_data is python dict so unpack dict
        #  so that it can be passed as arguments 


        #  becoz validate_data contains pswd without
        #  hashing so we hash pswd before saving ...
        return models.User.objects.create_user(**validated_data)





class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        attrs["user"] = user

        return attrs



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User

        fields = [
            "id",
            "username",
            "email",
            "city",
            "state",
            "phone_no",
            "profile_image",
            "first_name",
            "last_name",
        ]

        read_only_fields = [
            "id",
            "username",
        ]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    #  here value is of the field old_password..
    #  this functions is called by drf automaticly
    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )

        #  this will automaticaly add its value to 
        #  validated_data
        return value


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.CharField(
        source="author.username",
        read_only=True
    )

    replies = serializers.SerializerMethodField()

    class Meta:

        model = models.Comment

        fields = [
            "id",
            "author",
            "text",
            "created_date",
            "parent",
            "replies",
        ]

        read_only_fields = [
            "id",
            "author",
            "created_date",
        ]


    #  obj is the serialized comment obj ..
    def get_replies(self, obj):

        return CommentSerializer(
            obj.replies.all(),
            many=True
        ).data

    #  here parent is the comment object which 
    #  our serializer has converted from 
    #  parent id to comment obj  using our model 
     
    def validate_parent(self, parent):

        if parent is None:
            return parent

        post = self.context["post"]

        #  comment obj has fk as post so we can use orm here.
        if parent.post != post:
            raise serializers.ValidationError(
                "This comment does not belong to this post."
            )

        return parent

