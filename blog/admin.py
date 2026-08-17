from django.contrib import admin
from .models import Post
from django.contrib.auth.admin import UserAdmin
from .models import User , Category , Tag , Comment , Like

admin.site.register(Post)

# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')



admin.site.register(Tag)


admin.site.register(Comment)


admin.site.register(Like)


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