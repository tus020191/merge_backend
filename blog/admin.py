from django.contrib import admin
from .models import Post
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(Post)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": (
                "city",
                "state",
                "phone_no",
                "profile_image",
            ),
        }),
    )

    list_display = (
        "username",
        "email",
        "city",
        "state",
        "phone_no",
        "is_staff",
    )