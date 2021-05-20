from django.http import JsonResponse
from django.shortcuts import render
from .models import Markers, Reviews
from statistics import mean

from django.forms.models import model_to_dict


# Create your views here.
def index(request):
    markers = Markers.objects.all()
    return render(request, template_name='home/index.html', context={'markers': markers})


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
        ob = Reviews.objects.create(marker_id=id)
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
        ob.save()
        update_marker(id)

    reviews = ob
    return render(request, template_name='home/index.html', context={'reviews': reviews})

def update_marker(id):
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
    for x in rev:
        fin.append(x.financial_rating)
        avg.append(x.avg_cost)
        covid.append(x.covid_rating)
        bed.append(x.beds_available)
        care.append(x.care_rating)
        if x.oxygen_rating!=0:
            oxy.append(x.oxygen_rating-1)
        if x.ventilator_availability!=0:
            vent.append(x.ventilator_availability-1)
        if x.oxygen_availability!=0:
            oxya.append(x.oxygen_availability-1)
        if x.icu_availability!=0:
            icu.append(x.icu_availability-1)

    ob.financial_rating = round(mean(fin),1)
    ob.avg_cost = mean(avg)
    ob.covid_rating =round(mean(covid),1)
    ob.beds_available = sum(bed)
    ob.care_rating =round(mean(care),1)
    ob.oxygen_rating = round(mean(oxy),1)
    ob.ventilator_availability = round(sum(vent)*100/len(vent),2)
    ob.oxygen_availability = round(sum(oxya)*100/len(oxya),2)
    ob.icu_availability = round(sum(icu)*100/len(icu),2)
    ob.save()



