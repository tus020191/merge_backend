from rest_framework.permissions import BasePermission


class IsAuthorOrStaff(BasePermission):

    #  here obj is the object whose slug we have 
    #  passed in our url 

    #  view is the view set we are using or where this 
    #  IsAuthor is called .. that view ..
    def has_object_permission(self, request, view, obj):

        return (
            obj.author == request.user 
            or
            request.user.is_staff 
        )


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_staff
        )