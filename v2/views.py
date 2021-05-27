import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


# Create your views here.
def index(request):
    context = {}
    ipaddress = get_client_ip(request)
    context['ip'] = ipaddress
    return render(request, template_name='v2/index.html', context=context)


def signin(request):
    context1 = {}
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]
        if not email or not password:
            context1['pswderr'] = "Text fields cannot be empty"
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/v2/')
        else:
            # Return an 'invalid login' error message.
            context1['pswderr'] = "Invalid Credentials"
    context1['sign_text'] = 'Sign In'
    return render(request, template_name="v2/login.html", context=context1)


def signup(request):
    context1 = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        passwrd2 = request.POST["password retype"]
        if not email:
            context1['pswderr'] = 'Email cannot be empty'
        elif not password or not passwrd2:
            context1['pswderr'] = 'Password cannot be empty'
        else:
            if passwrd2 == password:
                try:
                    user = User.objects.create_user(email=email, password=password, username=email)
                    login(request, user)
                    return HttpResponseRedirect('/v2/')

                except Exception as e:
                    print(e)
                    context1['pswderr'] = 'User already exists'
            else:
                context1['pswderr'] = 'Password Does not match'
    context1['sign_text'] = "Register"
    return render(request, template_name="v2/signup.html", context=context1)


def get_location(request):
    ip = get_client_ip(request)
    ipsearchurl = f'https://ipapi.co/{ip}/json/'
    loc_data = requests.get(ipsearchurl, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
    return JsonResponse(json.loads(loc_data.content))
