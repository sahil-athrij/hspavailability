from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Markers, Reviews, SuspiciousMarking
import datetime
from django.forms.models import model_to_dict
from django.core import serializers


# Create your views here.
def index(request):
    return render(request, template_name='home/index.html')


def modify(request):
    if request.method == 'POST':

        print(request.POST)

        if int(request.POST['id']) != -1:
            ob = Markers.objects.get(id=int(request.POST['id']))
        else:
            ob = Markers.objects.create()
        ob.name = request.POST['name']
        ob.Phone = request.POST['phone']
        ob.size = int(request.POST['size'])
        ob.financial_rating = int(request.POST['financial'])
        ob.avg_cost = int(request.POST['cost'])
        ob.covid_rating = int(request.POST['covid'])
        ob.beds_available = int(request.POST['beds'])
        ob.care_rating = int(request.POST['care'])
        ob.oxygen_rating = int(request.POST['oxy'])
        ob.ventilator_availability = int(request.POST['vent'])
        ob.oxygen_availability = int(request.POST['oxya'])
        ob.icu_availability = int(request.POST['icu'])
        ob.lat = float(request.POST['lat'])
        ob.lng = float(request.POST['lng'])
        ob.datef = request.POST['datef']
        ob.added_by = request.user
        if 'hospital_pic' in request.FILES:
            ob.hospital_pic = request.FILES['hospital_pic']

        ob.save()

    markers = Markers.objects.all()
    return render(request, template_name='home/forms.html', context={'markers': markers})


def more_info(request, key_id):
    ob = Markers.objects.get(id=key_id)
    return JsonResponse(model_to_dict(ob))


def add_review(request):
    if request.method == 'POST':
        print(request.POST)
        id = int(request.POST['id'])
        mob = Markers.objects.get(id=id)
        user = request.user
        ob = Reviews.objects.create(marker_id=id, written_by=user)
        ob.financial_rating = int(request.POST['financial'])
        ob.avg_cost = int(request.POST['cost'])
        ob.covid_rating = int(request.POST['covid'])
        ob.beds_available = int(request.POST['beds'])
        ob.care_rating = int(request.POST['care'])
        ob.oxygen_rating = int(request.POST['oxy'])
        ob.ventilator_availability = int(request.POST['vent'])
        ob.oxygen_availability = int(request.POST['oxya'])
        ob.icu_availability = int(request.POST['icu'])
        ob.comment = request.POST['comment']
        d = ob.datef - mob.datef
        ob.day = d.days
        ob.save()
        if 'review_pic' in request.Files:
            pass
        update_marker(id)

    return HttpResponseRedirect('/')


def update_marker(id):
    """
    formula for each attribute = Σ(0.99^(x)*sum(data of x days before))/Σ(0.99^x)
    """
    ob = Markers.objects.get(id=id)
    rev = Reviews.objects.filter(marker__id=id)
    fin = []
    avg = []
    covid = []
    bed = []
    care = []
    oxy = []
    vent = []
    oxya = []
    icu = []
    day = []
    den = []
    deno = []
    denv = []
    deni = []
    denoa = []
    for x in rev:
        day.append(x.day)
    dmax = max(day)
    for x in rev:
        d = 0.99 ** (dmax - x.day)
        den.append(d)
        fin.append(d * x.financial_rating)
        avg.append(d * x.avg_cost)
        covid.append(d * x.covid_rating)
        bed.append(d * x.beds_available)
        care.append(d * x.care_rating)
        if x.oxygen_rating != 0:
            oxy.append(d * (x.oxygen_rating))
            deno.append(d)
        if x.ventilator_availability != 0:
            vent.append(d * (x.ventilator_availability - 1))
            denv.append(d)
        if x.oxygen_availability != 0:
            oxya.append(d * (x.oxygen_availability - 1))
            denoa.append(d)
        if x.icu_availability != 0:
            icu.append(d * (x.icu_availability - 1))
            deni.append(d)
    dens = sum(den)
    ob.financial_rating = round(sum(fin) / dens, 1)
    ob.avg_cost = sum(avg) / dens
    ob.covid_rating = round(sum(covid) / dens, 1)
    ob.beds_available = sum(bed)
    ob.care_rating = round(sum(care) / dens, 1)
    ob.oxygen_rating = round(sum(oxy) / sum(deno), 1)
    ob.ventilator_availability = round(sum(vent) * 100 / sum(denv), 2)
    ob.oxygen_availability = round(sum(oxya) * 100 / sum(denoa), 2)
    ob.icu_availability = round(sum(icu) * 100 / sum(deni), 2)
    ob.save()


def filter_marker(request):
    if request.method == "GET":
        fin = int(request.GET.get('financialfr', 0))
        costmin = request.GET.get('price-min', 0)
        costmax = request.GET.get('price-max', 1000000)
        covid = int(request.GET.get('covidfr', 0))
        beds = request.GET.get('bedsfr', 0)
        care = int(request.GET.get('carefr', 0))
        oxy = int(request.GET.get('oxyfr', 0))
        vent = request.GET.get('ventfr', 0)
        oxya = request.GET.get('oxyafr', 0)
        icu = request.GET.get('icufr', 0)
        markers = Markers.objects.filter(financial_rating__gte=fin,
                                         avg_cost__gte=costmin,
                                         avg_cost__lte=costmax,
                                         covid_rating__gte=covid,
                                         beds_available__gte=beds,
                                         care_rating__gte=care,
                                         oxygen_rating__gte=oxy,
                                         ventilator_availability__gte=vent,
                                         oxygen_availability__gte=oxya,
                                         icu_availability__gte=icu
                                         )

        return render(request, template_name='home/index.html', context={'markers': markers})

    return render(request, template_name='home/index.html')


def marker_nearby(request):
    if request.method == "POST":
        print(request)
        lat = float(request.POST['lat'])
        lng = float(request.POST['lng'])
        print(lat, lng)
        marker = Markers.objects.filter(lat__gte=lat - 1,
                                        lat__lte=lat + 1,
                                        lng__gte=lng - 1,
                                        lng__lte=lng + 1)
        marker_json = []
        for i in marker:
            marker_json.append(model_to_dict(i))
        return JsonResponse(marker_json, safe=False)

    return render(request, template_name='home/index.html')


def suspicious(request):
    if request.method == "POST":
        print(request.POST)
        id = int(request.POST['id'])
        mob = Markers.objects.get(id=id)
        user = request.user
        ob = SuspiciousMarking.objects.create(marker_id=id, created_by=user, comment=request.POST['comments'])
        ob.save()
        mob.Suspicious += 1
        mob.save()

    return HttpResponseRedirect('/')
