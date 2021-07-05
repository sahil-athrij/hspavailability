import json
from pprint import pprint
from urllib import parse

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from oauth2_provider.models import AccessToken, Application

from home.models import Tokens


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


# Create your views here.
@ensure_csrf_cookie
def index(request):
    context = {}
    ipaddress = get_client_ip(request)
    context['ip'] = ipaddress
    context['searchbar'] = True

    return render(request, template_name='v2/index.html', context=context)


@ensure_csrf_cookie
def signin(request):
    context1 = {}
    print("Hello There")
    pprint(request.META['QUERY_STRING'])
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
            redirect_location = request.GET.get('next', '/') + '?' + request.META['QUERY_STRING']

            print(redirect_location)
            return HttpResponseRedirect(redirect_location)
        else:
            # Return an 'invalid login' error message.
            context1['pswderr'] = "Invalid Credentials"
    context1['sign_text'] = 'Sign In'
    context1['GOOGLE_CLIENT_ID'] = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    scheme = "http://" if request.META.get('HTTP_HOST') == '127.0.0.1:8000' else "https://"
    context1['redirect_uri'] = scheme + request.META.get('HTTP_HOST') + '/google-login'
    return render(request, template_name="v2/login.html", context=context1)


@ensure_csrf_cookie
def signup(request):
    context1 = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        passwrd2 = request.POST.get("password retype")
        username = request.POST.get("username", '')
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        if not email:
            context1['pswderr'] = 'Email cannot be empty'
        elif not password or not passwrd2:
            context1['pswderr'] = 'Password cannot be empty'
        elif not username:
            context1['pswderr'] = 'Username cannot be empty'
        else:
            if passwrd2 == password:
                try:
                    user = User.objects.create_user(email=email, password=password, username=username,
                                                    first_name=firstname, last_name=lastname)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    print(request.GET.__dict__)
                    inv = request.POST.get('invite', '')
                    Tokens.objects.create(user=user, invite_token=inv)
                    invited = Tokens.objects.get(private_token=inv)
                    invited.invited += 1
                    invited.points += 10
                    invited.save()

                    redirect_location = request.GET.get('next', '/') + '?' + request.META['QUERY_STRING']
                    return HttpResponseRedirect(redirect_location)

                except User.DoesNotExist as e:
                    print(e)
                    context1['pswderr'] = 'User already exists'
                except Tokens.DoesNotExist as e:
                    print(e)
                    context1['pswderr'] = 'Invite Code is invalid'

            else:
                context1['pswderr'] = 'Password Does not match'
    context1['sign_text'] = "Register"
    next_loc = request.GET.get('next', '')
    parsed = parse.parse_qs(next_loc)
    next_loc = dict(parsed)
    print(next_loc)
    try:
        context1['invite'] = next_loc["invite"][0]
    except:
        context1['invite'] = ''
    context1['GOOGLE_CLIENT_ID'] = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    scheme = "http://" if request.META.get('HTTP_HOST') == '127.0.0.1:8000' else "https://"
    context1['redirect_uri'] = scheme + request.META.get('HTTP_HOST') + '/google-login'
    return render(request, template_name="v2/signup.html", context=context1)


@login_required
def log_out(request):
    logout(request)
    url = '/?' + request.META['QUERY_STRING']
    return HttpResponseRedirect(url)


@ensure_csrf_cookie
def help_page(request):
    return render(request, template_name='v2/help.html')


def request_google(auth_code, redirect_uri):
    data = {'code': auth_code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    try:
        pprint(r.content.decode())
        content = json.loads(r.content.decode())
        token = content["access_token"]
        return token
    except Exception as e:
        print(e)
        return False


def convert_google_token(baseUrl, token, client_id):
    application = Application.objects.get(client_id=client_id)

    data = {
        'grant_type': 'convert_token',
        'client_id': client_id,
        'client_secret': application.client_secret,
        'backend': 'google-oauth2',
        'token': token
    }
    url = baseUrl + '/auth/social/convert-token'
    r = requests.post(url, data=data)
    try:
        cont = json.loads(r.content.decode())
        print(cont)
        access_token = cont['access_token']
        return access_token
    except Exception as e:
        print(e)
        return False


def Google_login(request):
    next_loc = request.GET.get('state', False)
    auth_code = request.GET.get('code')
    client_id = settings.DEFAULT_CLIENT
    scheme = "http://" if request.META.get('HTTP_HOST') == '127.0.0.1:8000' else "https://"
    baseUrl = scheme + request.META.get('HTTP_HOST')
    redirect_uri = baseUrl + '/google-login'
    if next_loc:
        parsed = parse.parse_qs(next_loc)
        next_loc = dict(parsed)
        next_loc = next_loc['next'][0]
        search_query = next_loc.split('?')[1]
        parsed_token = parse.parse_qs(search_query)
        original_query = dict(parsed_token)
        print(original_query)
        client_id = original_query['client_id'][0]
    token = request_google(auth_code, redirect_uri)
    print(token)
    if token:
        access_token = convert_google_token(baseUrl, token, client_id)
        if access_token:
            user = AccessToken.objects.get(token=access_token).user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if next_loc:
                try:
                    token = original_query['invite'][0]
                    invited = Tokens.objects.get(private_token=token)
                    Tokens.objects.create(user=user, invite_token=token)
                    invited.points += 10
                    invited.invited += 1
                    invited.save()
                except Exception as e:
                    print(e)
                print(next_loc)
                return HttpResponseRedirect(next_loc)
            else:
                return HttpResponseRedirect('/')

    return HttpResponseRedirect('/login/')
