from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#  user defiend modules
from .models import Post , User , Category, Tag
from .forms import PostForm

def post_list(request):

    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    posts = Post.objects.all()

    contextDictionary = {
        "posts" : posts
    }


    return render(request, 'blog/post_list.html', contextDictionary)


def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    # this will be for right pannel to display all categories 
    #  for filter purpose 
    categories = Category.objects.all()

    #  same as for categories  above 
    tags = Tag.objects.all()

    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
            'categories': categories,
            'tags': tags,
        }
    )



def post_new(request):
    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(
        request.POST,
        request.FILES,
        instance=post
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f"welcome {user.username} Login Successful!")
            return redirect("post_list")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "blog/login.html")

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        city = request.POST.get("city")
        state = request.POST.get("state")
        phone_no = request.POST.get("phone_no")

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        profile_image = request.FILES.get("profile_image")

        # Check username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request,"blog/signup.html")

        # Check email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request,"blog/signup.html")

        # Check password
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request,"blog/signup.html")

        # Create user with hash pswd instead of objects.create()
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1,
        )

        # Save custom fields
        user.city = city
        user.state = state
        user.phone_no = phone_no
        user.profile_image = profile_image

        user.save()

        messages.success(request, "Account created successfully!")

        login(request, user)

        return redirect("post_list")

    return render(request, "blog/signup.html")

@login_required
def profile(request):
    # user = request.user
    # print(user.profile_image.url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    return render(request, "blog/profile.html")



@login_required
def edit_profile(request):

    if request.method == "POST":

        user = request.user

        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.phone_no = request.POST.get("phone_no")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        messages.success(request, "Profile updated successfully!")

        return redirect("profile")

    return render(request, "blog/edit_profile.html")



def user_logout(request):
    logout(request)

    messages.success(request, "logout  successfully!")

    return redirect("post_list")