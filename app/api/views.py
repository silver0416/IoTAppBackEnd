from asyncio import protocols
import requests
from django.shortcuts import render
from django.contrib import messages
from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes,
)
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .forms import resetPassword
# Create your views here.


@api_view(["GET"])
@permission_classes([AllowAny])
def request_user_activation(request, uid, token):
    """ 
    Intermediate view to activate a user's email. 
    """
    # protocol = 'https://'
    protocol = 'http://'
    web_url = protocol + request.get_host()
    post_url = web_url + "/auth/users/activation/"
    post_data = {"uid": uid, "token": token}
    requests.post(post_url, data=post_data)
    messages.success(request, '信箱啟用成功!')
    return render(request, "activation_success.html")

@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes([AllowAny])
def reset_user_password(request, **kwargs):
    # uses djoser to reset password
    if request.POST:
        current_site = request.get_host()
        # Site.objects.get_current()
        # #names of the inputs in the password reset form
        password = request.POST.get('new_password')
        password_confirmation = request.POST.get('re_new_password')
        #data to accept. the uid and token is obtained as keyword arguments in the url
        payload = {
            'uid': kwargs.get('uid'),
            'token': kwargs.get('token'),
            'new_password': password,
            're_new_password': password_confirmation
        }

        djoser_password_reset_url = '/auth/users/reset_password_confirm/'
        # protocol = 'https'
        protocol = 'http'
        url = '{0}://{1}/{2}'.format(protocol, current_site,
                                     djoser_password_reset_url)
        response = requests.post(url,data=payload)

        if response.status_code == 204:
            # Give some feedback to the user.
            messages.success(request,
                             '重設密碼成功!')
            return render(request, "reset_password.html")
        else:
            response_object = response.json()
            response_object_keys = response_object.keys()
            #catch any errors
            for key in response_object_keys:
                decoded_string = response_object.get(key)[0].replace("'", "\'")
                messages.error(request, f'{decoded_string}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # if the request method is a GET request, provide the template to show. in most cases, the password reset form.
    else:
        form = resetPassword()
        context = {'form': form}
        return render(request, 'password_reset_from_key.html',context)


def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})


def index(request):
    return render(request, 'index.html')


