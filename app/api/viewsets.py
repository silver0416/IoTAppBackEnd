from rest_framework import viewsets
# Create your views here.
from .models import *
from .serializers import *


class userViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = userSerializer


class user_belong_homeViewSet(viewsets.ModelViewSet):

    queryset = user_belong_home.objects.all()
    serializer_class = user_belong_homeSerializer


class home_listViewSet(viewsets.ModelViewSet):

    queryset = home_list.objects.all()
    serializer_class = home_listSerializer


class added_device_listViewSet(viewsets.ModelViewSet):

    queryset = added_device_list.objects.all()
    serializer_class = added_device_listSerializer


class device_typeViewSet(viewsets.ModelViewSet):

    queryset = device_type.objects.all()
    serializer_class = device_typeSerializer


class alive_verification_codeViewSet(viewsets.ModelViewSet):

    queryset = alive_verification_code.objects.all()
    serializer_class = alive_verification_codeSerializer


class categoryViewSet(viewsets.ModelViewSet):

    queryset = category_detail.objects.all()
    serializer_class = categorySerializer


class device_dataViewSet(viewsets.ModelViewSet):

    queryset = device_data.objects.all()
    serializer_class = device_dataSerializer