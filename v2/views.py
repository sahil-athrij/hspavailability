import json
import logging
import os
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

logger = logging.getLogger('v2')

def give_points(personal_token, option):
    """
     Throws Error if the invite code is invalid
    @param personal_token: str
    @type option: str
    """

    if personal_token and personal_token != 'null':
        invited = Tokens.objects.get(private_token=personal_token)
        if option == 'invite':
            invited.invited += 1
            invited.points += 10
        elif option == 'review':
            invited.reviews += 1
            invited.points += 5
        elif option == 'report':
            invited.reports += 1
            invited.points += 1
        invited.save()


def parse_url_next(next_loc):
    parsed = parse.parse_qs(next_loc)
    try:
        next_loc = dict(parsed)
        return next_loc
    except Exception as e:
        logger.exception("Parser")
        return False


def get_item_from_list_dict(parsed_loc, key):
    try:
        invite = parsed_loc[key][0]
    except (IndexError, KeyError) as e:
        logger.error('item not in list ' + str(e))
        invite = ''
        print(e)
    return invite


def get_item_from_url(url_params, key, default=''):
    parsed_loc = parse_url_next(url_params)
    if parsed_loc:
        return get_item_from_list_dict(parsed_loc, key)
    else:
        return default


def get_client_id(next_string):
    client_id = settings.DEFAULT_CLIENT
    if next_string:
        try:
            search_query = next_string.split('?')[1]
            client_id = get_item_from_url(search_query, 'client_id')
        except IndexError:
            logger.debug('client id was not provided')
    return client_id


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
            return HttpResponseRedirect(redirect_location)
        else:
            # Return an 'invalid login' error message.
            context1['pswderr'] = "Invalid Credentials"
    context1['sign_text'] = 'Sign In'
    context1['GOOGLE_CLIENT_ID'] = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    context1['redirect_uri'] = settings.DEPLOYMENT_URL + '/google-login'
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
            logger.info('Email was empty')
        elif not password or not passwrd2:
            context1['pswderr'] = 'Password cannot be empty'
            logger.info('Password was empty')
        elif not username:
            context1['pswderr'] = 'Username cannot be empty'
            logger.info('Username was empty')
        else:
            if passwrd2 == password:
                try:
                    inv = request.POST.get('invite', '')
                    give_points(inv, 'invite')
                    user = User.objects.create_user(email=email, password=password, username=username,
                                                    first_name=firstname, last_name=lastname)
                    Tokens.objects.get_or_create(user=user, invite_token=inv)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    redirect_location = request.GET.get('next', '/') + '?' + request.META['QUERY_STRING']
                    return HttpResponseRedirect(redirect_location)

                except User.DoesNotExist as e:
                    print(e)
                    logger.info('User already exist')
                    context1['pswderr'] = 'User already exists'
                except Tokens.DoesNotExist as e:
                    print(e)
                    logger.info('Token was invalid')
                    context1['pswderr'] = 'Invalid Token'

            else:
                logger.info('Password Does not match')
                context1['pswderr'] = 'Password Does not match'

    next_loc = request.GET.get('next', '')
    context1['sign_text'] = "Register"
    context1['invite'] = get_item_from_url(next_loc, 'invite')
    context1['redirect_uri'] = settings.DEPLOYMENT_URL + '/google-login'
    context1['GOOGLE_CLIENT_ID'] = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
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
    print(data)
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    try:
        logger.info('google auth ')
        content = json.loads(r.content.decode())
        token = content["access_token"]
        return token
    except Exception as e:
        logger.exception('google auth fail')
        print(e)
        return False


def convert_google_token(token, client_id):
    application = Application.objects.get(client_id=client_id)
    data = {
        'grant_type': 'convert_token',
        'client_id': client_id,
        'client_secret': application.client_secret,
        'backend': 'google-oauth2',
        'token': token
    }
    url = 'http://127.0.0.1:8000/auth/social/convert-token'
    r = requests.post(url, data=data)
    print(r.content)
    try:
        logger.info('google auth')
        cont = json.loads(r.content.decode())
        access_token = cont['access_token']
        return access_token
    except Exception as e:
        logger.exception('google convert')
        return False


def Google_login(request):
    state = request.GET.get('state', '/')
    auth_code = request.GET.get('code')
    redirect_uri = settings.DEPLOYMENT_URL + '/google-login'

    next_loc = get_item_from_url(state, 'next', '/')
    logger.info('next' + next_loc)
    invite_token = get_item_from_url(next_loc, 'invite')
    client_id = get_client_id(next_loc)
    token = request_google(auth_code, redirect_uri)
    if token:
        access_token = convert_google_token(token, client_id)

        if access_token:
            user = AccessToken.objects.get(token=access_token).user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            try:
                Tokens.objects.get_or_create(user=user, invite_token=invite_token)
            except:
                token = Tokens.objects.get(user_id=user.id)
                if not token.invite_token:
                    token.invite_token = invite_token
                    token.save()
            try:
                give_points(invite_token, 'invite')
            except Exception:
                logger.exception('tokens')

        return HttpResponseRedirect(next_loc)
    return HttpResponseRedirect('/login/')
