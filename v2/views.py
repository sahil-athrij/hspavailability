from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from home.models import *


# Create your views here.
def index(request):
    return render(request, template_name='v2/index.html')


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
        # beds = request.GET.get('bedsfr', 0)
        # print(beds)

        # context["search_results"] = Markers.objects.filter(financial_rating__gte=fin,
        #                                                    avg_cost__gte=costmin,
        #                                                    avg_cost__lte=costmax,
        #                                                    covid_rating__gte=covid,
        #                                                    beds_available__gte=beds,
        #                                                    care_rating__gte=care,
        #                                                    oxygen_rating__gte=oxy,
        #                                                    ventilator_availability__gte=vent,
        #                                                    oxygen_availability__gte=oxya,
        #                                                    icu_availability__gte=icu,
        #                                                    name__icontains=query
        #                                                    )

        context["search_results"] = Markers.objects.filter(financial_rating__gte=fin,
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

        return render(request, template_name='v2/search.html', context=context)

    return render(request, template_name='v2/index.html')
