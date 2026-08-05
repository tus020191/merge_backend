import os
import sys
import django


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)


django.setup()


from blog.models import Category, Tag, Post, User


class Dummy():

    help = "Seed dummy blog data"

    def handle(self):

        # Get an existing user
        user = User.objects.first()

        

        # -------------------------
        # Categories
        # -------------------------

        categories_data = [
            "Django",
            "Python",
            "Web Development",
            "JavaScript",
            "Career & Learning",
        ]

        categories = {}

        for name in categories_data:

            category, created = Category.objects.get_or_create(
                name=name
            )

            categories[name] = category

        # -------------------------
        # Tags
        # -------------------------

        tags_data = [
            "Django",
            "Python",
            "Backend",
            "Web Development",
            "Programming",
            "Beginner",
            "Tutorial",
            "Database",
            "REST API",
            "JavaScript",
            "Frontend",
            "Career",
            "Learning",
        ]

        tags = {}

        for name in tags_data:

            tag, created = Tag.objects.get_or_create(
                name=name
            )

            tags[name] = tag

        # -------------------------
        # Posts
        # -------------------------

        posts_data = [

            {
                "title": "Django Models Explained: A Beginner's Guide",

                "category": "Django",

                "tags": [
                    "Django",
                    "Python",
                    "Backend",
                    "Beginner",
                    "Tutorial",
                ],

                "text": """
Django models provide a powerful way to represent and manage data in a web application.

Instead of writing SQL queries for every database operation, developers can define their database structure using Python classes.

In this guide, we explore important Django concepts such as models, fields, migrations, ForeignKey relationships, and ManyToMany relationships.

Understanding these concepts is essential for building scalable Django applications.
""",
            },

            {
                "title": "Python Basics Every Beginner Should Learn",

                "category": "Python",

                "tags": [
                    "Python",
                    "Programming",
                    "Beginner",
                    "Learning",
                    "Tutorial",
                ],

                "text": """
Python is one of the most popular programming languages for beginners and professionals.

Its simple syntax makes it easy to learn, while its powerful libraries allow developers to build web applications, automation scripts, data analysis tools, and artificial intelligence systems.

If you are starting your programming journey, you should first understand variables, data types, conditional statements, loops, functions, and object-oriented programming.

Learning these fundamentals will give you a strong foundation for learning frameworks such as Django.
""",
            },

            {
                "title": "Understanding ForeignKey and ManyToManyField in Django",

                "category": "Django",

                "tags": [
                    "Django",
                    "Python",
                    "Database",
                    "Backend",
                    "Tutorial",
                ],

                "text": """
Database relationships are an important part of almost every web application.

Django makes it easy to create these relationships using fields such as ForeignKey and ManyToManyField.

A ForeignKey is useful when one object is related to another object. For example, one category can have many blog posts.

A ManyToManyField is useful when both sides can have multiple relationships. For example, one blog post can have multiple tags, and the same tag can be used by multiple blog posts.

Understanding these relationships helps developers design better database structures.
""",
            },

            {
                "title": "How to Build Your First Django Blog",

                "category": "Web Development",

                "tags": [
                    "Django",
                    "Python",
                    "Web Development",
                    "Backend",
                    "Beginner",
                ],

                "text": """
Building a blog is one of the best ways to learn Django.

A blog project allows you to work with models, views, templates, forms, authentication, media files, and database relationships.

In a typical Django blog, users can create posts, add categories and tags, upload images, and display their content through dynamic templates.

By building a complete project step by step, you can understand how the different parts of Django work together.
""",
            },

            {
                "title": "Django Authentication: Login, Signup and User Profiles",

                "category": "Django",

                "tags": [
                    "Django",
                    "Backend",
                    "Python",
                    "Tutorial",
                ],

                "text": """
Authentication is an important feature of modern web applications.

Django provides a powerful authentication system that allows developers to manage users, passwords, login sessions, and permissions.

In a blog application, users can create accounts, log in, update their profiles, and create or edit posts.

Django's authentication system provides the backend functionality while developers can create their own custom HTML forms and user interfaces.
""",
            },

            {
                "title": "Introduction to REST APIs with Django",

                "category": "Web Development",

                "tags": [
                    "Django",
                    "REST API",
                    "Backend",
                    "Python",
                    "Database",
                ],

                "text": """
REST APIs allow different applications to communicate with each other through HTTP requests.

They are commonly used to connect web applications, mobile applications, and frontend frameworks with backend services.

Django developers can build powerful APIs that provide data in JSON format.

Learning REST APIs is an important step for developers who want to build modern full-stack applications.
""",
            },

            {
                "title": "JavaScript Fundamentals for Web Developers",

                "category": "JavaScript",

                "tags": [
                    "JavaScript",
                    "Frontend",
                    "Programming",
                    "Beginner",
                    "Web Development",
                ],

                "text": """
JavaScript is one of the most important technologies used in modern web development.

While HTML provides structure and CSS provides styling, JavaScript adds interactivity and dynamic behavior to websites.

Beginners should start by learning variables, functions, arrays, objects, loops, events, and DOM manipulation.

Once these fundamentals are clear, developers can move on to modern technologies such as React.
""",
            },

            {
                "title": "Frontend vs Backend Development: What Should You Learn?",

                "category": "Career & Learning",

                "tags": [
                    "Frontend",
                    "Backend",
                    "Web Development",
                    "Learning",
                    "Career",
                ],

                "text": """
Frontend and backend development are two important parts of modern web applications.

Frontend development focuses on everything users see and interact with in the browser.

Backend development handles server-side logic, databases, authentication, and APIs.

Both areas offer excellent career opportunities. The best choice depends on your interests and the type of applications you want to build.

Many developers eventually learn both areas and become full-stack developers.
""",
            },

        ]

        # -------------------------
        # Create Posts
        # -------------------------

        for data in posts_data:

            post, created = Post.objects.get_or_create(

                title=data["title"],

                defaults={
                    "author": user,
                    "category": categories[data["category"]],
                    "text": data["text"].strip(),
                }

            )

            if created:

                post.tags.set(
                    [
                        tags[tag_name]
                        for tag_name in data["tags"]
                    ]
                )

            else:

                print("already exist")

        

dummy = Dummy()

dummy.handle()