import json
from pprint import pprint
from urllib import parse
from uuid import uuid4

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from oauth2_provider.models import AccessToken

from home.models import Markers, Reviews


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
            redirect_location = request.GET.get('next', '/')

            print(redirect_location)
            return HttpResponseRedirect(redirect_location)
        else:
            # Return an 'invalid login' error message.
            context1['pswderr'] = "Invalid Credentials"
    context1['sign_text'] = 'Sign In'
    return render(request, template_name="v2/login.html", context=context1)


@ensure_csrf_cookie
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
                    try:
                        inv = request.GET["invite_token"]
                    except:
                        inv = ""
                    Tokens.objects.create(User=user, private_token=uuid4, invite_token=inv)
                    redirect_location = request.GET.get('next=', '/')
                    return HttpResponseRedirect(redirect_location)

                except Exception as e:
                    print(e)
                    context1['pswderr'] = 'User already exists'
            else:
                context1['pswderr'] = 'Password Does not match'
    context1['sign_text'] = "Register"

    return render(request, template_name="v2/signup.html", context=context1)


@login_required
def log_out(request):
    logout(request)
    url = '/?' + request.META['QUERY_STRING']
    return HttpResponseRedirect(url)


@ensure_csrf_cookie
def search(request):
    if (request.method == "GET"):
        template_name = "v2/search.html"
        context = {}
        query = request.GET["query"]
        oxy = int(request.GET.get('oxyfr', 0))
        print(oxy)
        fin = int(request.GET.get('financialfr', 0))
        print(fin)
        vent = request.GET.get('ventfr', 0)
        print(vent)
        oxya = request.GET.get('oxyafr', 0)
        print(oxya)
        icu = request.GET.get('icufr', 0)
        print(icu)
        costmax = request.GET.get('price-max', 1000000)
        print(costmax)
        costmin = request.GET.get('price-min', 0)
        print(costmin)
        care = int(request.GET.get('carefr', 0))
        print(care)
        covid = int(request.GET.get('covidfr', 0))
        print(covid)
        try:
            lat = float(request.GET.get('lat', 0))
            lng = float(request.GET.get('lng', 0))
        except:
            lat = 0
            lng = 0
        if lat == 0 and lng == 0:
            data = get_loction_python(request)
            print(data)
            try:
                lat = float(data['latitude'])
                lng = float(data['longitude'])
            except Exception as e:
                print(e)
        print(lat, lng)
        queryset = Markers.objects.filter(

            financial_rating__gte=fin,
            avg_cost__gte=costmin,
            avg_cost__lte=costmax,
            covid_rating__gte=covid,
            care_rating__gte=care,
            oxygen_rating__gte=oxy,
            ventilator_availability__gte=vent,
            oxygen_availability__gte=oxya,
            icu_availability__gte=icu,
            name__icontains=query
        )
        loc = Point(lng, lat, srid=4326)
        if queryset.count() > 400:
            queryset = queryset.filter(lat__gte=lat - 0.5,
                                       lat__lte=lat + 0.5,
                                       lng__gte=lng - 0.5,
                                       lng__lte=lng + 0.5, )
        queryset = queryset.filter(location__distance_lte=(loc, D(m=10000000))).annotate(
            distance=Distance('location', loc)).order_by('distance')[:10]

        context["search_results"] = queryset
        print(context)
        ipaddress = get_client_ip(request)
        context['ip'] = ipaddress

        return render(request, template_name='v2/search.html', context=context)

    return render(request, template_name='v2/index.html')


def get_loction_python(request):
    ip = get_client_ip(request)
    ipsearchurl = f'https://ipapi.co/{ip}/json/'
    loc_data = requests.get(ipsearchurl, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
    return json.loads(loc_data.content)


def get_location(request):
    loc_data = get_loction_python(request)
    return JsonResponse(loc_data)


@ensure_csrf_cookie
def details(request, hospital_id):
    context = {}
    query = Markers.objects.get(id=hospital_id)
    review = Reviews.objects.filter(marker=hospital_id)
    context['hospital'] = query
    open_review = request.GET.get('review', 0)
    stuff = review.values()
    context["reviews"] = review
    context["open_review"] = open_review
    return render(request, template_name='v2/details.html', context=context)


@ensure_csrf_cookie
def help_page(request):
    return render(request, template_name='v2/help.html')


@ensure_csrf_cookie
def addHospital(request):
    return render(request, template_name='v2/addhospital.html')


def Google_login(request):
    auth_code = request.GET.get('code')
    print(auth_code)
    redirect_uri = 'http://127.0.0.1:8000/google-login'
    data = {'code': auth_code,
            'client_id': '569002618626-kr65dimckmmdbgfuafrakqa0g6h18f55.apps.googleusercontent.com',
            'client_secret': 'w_424dxoSAR5m9l-Xl9nOIwH',
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    print('access code', r.content)
    content = json.loads(r.content.decode())
    token = content["access_token"]
    print('Token=', token)
    data = {
        'grant_type': 'convert_token',
        'client_id': '6tWdAZrlxUA26FJSMjE7oKBpTNGaqJRl2bsmNMRb',
        'client_secret': 'mwFcVOr4NicFnxlTDHRy5h48tbj3ohsJ5HxOIs0juJEmwQ25r8hByHkn9qqsMudm2Qju4Qh57117PHIPJTSupLNNTspcvwdDovM1P7Icw9PEwdcJ1djLCU5PbruqeSWv',
        'backend': 'google-oauth2',
        'token': token
    }
    url = 'http://127.0.0.1:8000/auth/social/convert-token'
    r = requests.post(url, data=data)
    try:
        cont = json.loads(r.content.decode())
        print(cont)
    except:
        return HttpResponse(r.content)
    access_token = cont['access_token']
    user = AccessToken.objects.get(token=access_token).user
    print(user)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    next = request.GET.get('state', False)
    if next:
        parsed = parse.parse_qs(next)
        next = dict(parsed)
        next = next['next'][0]
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/')


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


def ping(request):
    return JsonResponse({'result': 'OK'})
