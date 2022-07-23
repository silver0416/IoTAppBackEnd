from cmath import inf
from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from api.models import user_belong_home, user_info,home_list,added_device_list,device_type,alive_verification_code,category_detail
from api.serializers import user_infoSerializer,user_belong_homeSerializer,home_listSerializer,added_device_listSerializer,device_typeSerializer,alive_verification_codeSerializer,categorySerializer

class user_infoViewSet(viewsets.ModelViewSet):

    queryset = user_info.objects.all()
    serializer_class = user_infoSerializer

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

