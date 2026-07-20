from django import forms
from .models import Post , Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            "category",
            "title",
            "thumbnail",
            "featured_image",
            "text",
            "tags",
        )

class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        # We only include text because 
        # these fields should be assigned automatically:

        # post → current post
        # author → logged-in user
        # parent → comment being replied to
        fields = [
            "text"
        ]

        widgets = {

            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "content..."
                }
            )

        }