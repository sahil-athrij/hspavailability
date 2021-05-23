from django.http import JsonResponse
from django.shortcuts import render
from .models import Markers, Reviews
import datetime
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
        ob.datef = request.POST['datef']
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
        d = ob.datef-mob.datef
        ob.day = d.days
        ob.save()
        update_marker(id)

    reviews = ob
    return render(request, template_name='home/index.html', context={'reviews': reviews})

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
    denoa =[]
    for x in rev:
        day.append(x.day)
    dmax = max(day)
    for x in rev:
        d=0.99**(dmax-x.day)
        den.append(d)
        fin.append(d*x.financial_rating)
        avg.append(d*x.avg_cost)
        covid.append(d*x.covid_rating)
        bed.append(d*x.beds_available)
        care.append(d*x.care_rating)
        if x.oxygen_rating!=0:
            oxy.append(d*(x.oxygen_rating))
            deno.append(d)
        if x.ventilator_availability!=0:
            vent.append(d*(x.ventilator_availability-1))
            denv.append(d)
        if x.oxygen_availability!=0:
            oxya.append(d*(x.oxygen_availability-1))
            denoa.append(d)
        if x.icu_availability!=0:
            icu.append(d*(x.icu_availability-1))
            deni.append(d)
    dens = sum(den)
    ob.financial_rating = round(sum(fin)/dens,1)
    ob.avg_cost = sum(avg)/dens
    ob.covid_rating =round(sum(covid)/dens,1)
    ob.beds_available = sum(bed)
    ob.care_rating =round(sum(care)/dens,1)
    ob.oxygen_rating = round(sum(oxy)/sum(deno),1)
    ob.ventilator_availability = round(sum(vent)*100/sum(denv),2)
    ob.oxygen_availability = round(sum(oxya)*100/sum(denoa),2)
    ob.icu_availability = round(sum(icu)*100/sum(deni),2)
    ob.save()



