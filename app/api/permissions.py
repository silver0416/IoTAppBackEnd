from rest_framework import permissions
from .models import *
from rest_framework.exceptions import APIException
from rest_framework import status

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # print(obj.home_id)

        # Write permissions are only allowed to the owner of the snippet.
        return (
            request.user
            in home_list.objects.filter(home_id=obj.home_id).get().user.all()
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "非該家庭管理員無法設定"
    def has_permission(self, request, view):
        # print(home_admin.objects.filter(admin=request.user).exists())
        if home_admin.objects.filter(admin=request.user).exists():
            return True
        return False

   
    