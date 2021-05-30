import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from home.models import *


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
    context['searchbar'] = True

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
        print(lat,lng)
        context["search_results"] = Markers.objects.filter(
            lat__gte=lat - 0.5,
            lat__lte=lat + 0.5,
            lng__gte=lng - 0.5,
            lng__lte=lng + 0.5,
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


def details(request, hospital_id):
    context = {}
    query = Markers.objects.get(id=hospital_id)
    review = Reviews.objects.filter(marker=hospital_id)
    context['hospital'] = query
    stuff = review.values()
    context["reviews"] = review
    return render(request, template_name='v2/details.html', context=context)
