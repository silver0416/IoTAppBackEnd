from rest_framework import viewsets

# Create your views here.
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import Http404


class homeAdminViewSet(viewsets.ModelViewSet):

    queryset = home_admin.objects.all()

    serializer_class = homeAdminSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {"message": "錯誤請求，不能直接新增家庭管理員"}, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        home_obj = home_list.objects.filter(home_id=self.get_object().home_id).get()
        admin = User.objects.get(username=request.data.get("admin"))
        if admin not in home_obj.user.all():
             return Response(
                {"message": "錯誤請求，使用者不在這個家庭裡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = queryset.filter(admin=self.request.user)
        return queryset


class homeViewSet(viewsets.ModelViewSet):

    queryset = home_list.objects.all()
    serializer_class = homeSerializer
    permission_classes_by_action = {
        "destroy": [permissions.IsAuthenticated, IsOwnerOrReadOnly, IsAdminOrReadOnly],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):

        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            request_user = list(
                map(
                    lambda x: User.objects.filter(username=x).get(),
                    request.data.get("user"),
                )
            )
        except:
            request_user = list(
                map(
                    lambda x: User.objects.filter(username=x).get(),
                    request.data.getlist("user"),
                )
            )
        if (len(request_user)) > 1 or request.user not in request_user:
            return Response(
                {"message": "尚未建立家庭，無法加人"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        current_home = home_list.objects.filter(
            home_id=serializer.data.get("home_id")
        ).get()
        home_admin.objects.create(home=current_home, admin=request.user)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        # let admin user cannot delete itself
        object_id = kwargs.get("pk")
        admin = home_admin.objects.filter(home_id=object_id).get()
        home = home_list.objects.filter(home_id=object_id).get()
        try:
            request_user = list(
                map(
                    lambda x: User.objects.filter(username=x).get(),
                    request.data.get("user"),
                )
            )
        except:
            request_user = list(
                map(
                    lambda x: User.objects.filter(username=x).get(),
                    request.data.getlist("user"),
                )
            )
        if admin.admin not in request_user:
            return Response(
                {"message": "錯誤請求，管理員不能退出家庭"}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.user != admin.admin:
            if len(request_user) <= len(home.user.all()):
                if (
                    len(request_user) != len(home.user.all()) - 1
                    or request.user in request_user
                ):
                    return Response(
                        {"message": "權限不足，你無法退出其他成員"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        return super().update(request, *args, **kwargs)


class added_device_listViewSet(viewsets.ModelViewSet):

    queryset = device_list.objects.all()
    serializer_class = device_listSerializer


class device_typeViewSet(viewsets.ModelViewSet):

    queryset = device_type.objects.all()
    serializer_class = device_typeSerializer


class device_dataViewSet(viewsets.ModelViewSet):

    queryset = device_data.objects.all()
    serializer_class = device_dataSerializer


class mode_key_dataViewSet(viewsets.ModelViewSet):

    queryset = mode_key_data.objects.all()
    serializer_class = mode_key_dataSerializer
