from django.http import HttpResponse
from IoTAppBackEnd import database

# Create your views here.
def hello(request):
    
    tt = database.account.get_username(1)

    return HttpResponse(f'Hello World ! {tt}')