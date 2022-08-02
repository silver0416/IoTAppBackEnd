from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import permissions

# Create your views here.


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def request_user_activation(request, uid, token):
    """ 
    Intermediate view to activate a user's email. 
    """
    protocol = 'https://' if request.is_secure() else 'http://'
    web_url = protocol + request.get_host()
    post_url = web_url + "/auth/users/activation/"
    post_data = {"uid": uid, "token": token}
    result = requests.post(post_url, data=post_data)
    content = result.text+"信箱啟用成功"
    return Response(content)