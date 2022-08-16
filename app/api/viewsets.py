from rest_framework import viewsets

# Create your views here.
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class homeAdminViewSet(viewsets.ModelViewSet):

    queryset = home_admin.objects.all()

    serializer_class = homeAdminSerializer

    def create(self, request, *args, **kwargs):
        queryset = home_list.objects.all()
        serializer = homeSerializer(queryset, many=True)
        home_id = request.data.get("home")
        home_obj = home_list.objects.filter(home_id=home_id).get()
        admin = User.objects.get(user_uid=request.data.get("admin"))
        if admin in home_obj.user.all():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(
                {"message": "admin is not in this home"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class homeViewSet(viewsets.ModelViewSet):

    queryset = home_list.objects.all()
    serializer_class = homeSerializer


class added_device_listViewSet(viewsets.ModelViewSet):

    queryset = added_device_list.objects.all()
    serializer_class = added_device_listSerializer


class device_typeViewSet(viewsets.ModelViewSet):

    queryset = device_type.objects.all()
    serializer_class = device_typeSerializer


class categoryViewSet(viewsets.ModelViewSet):

    queryset = category_detail.objects.all()
    serializer_class = categorySerializer


class device_dataViewSet(viewsets.ModelViewSet):

    queryset = device_data.objects.all()
    serializer_class = device_dataSerializer

class mode_key_dataViewSet(viewsets.ModelViewSet):
    
    queryset = mode_key_data.objects.all()
    serializer_class = mode_key_dataSerializer
