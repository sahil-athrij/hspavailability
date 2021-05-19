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
        ob.comment = request.POST['comment']
        ob.save()
        update_marker(id)

def update_marker(id):
    ob = Markers.objects.get(id)
    rev = Reviews.objects.filter(marker__id=id)
    fin = []
    for x in rev.financial_rating:fin.append(x)
    ob.financial_rating = mean(fin)
    avg = []
    for x in rev.avg_cost:avg.append(x)
    ob.avg_cost = mean(avg)
    covid = []
    for x in rev.covid_rating:covid.append(x)
    ob.covid_rating = mean(covid)
    bed = []
    for x in rev.beds_available:bed.append(x)
    ob.beds_available = sum(bed)
    care = []
    for x in rev.care_rating:care.append(x)
    ob.care_rating = mean(care)
    oxy = []
    for x in rev.oxygen_rating:oxy.append(x)
    ob.avg_cost = mean(oxy)
    vent = []
    for x in rev.ventilator_availability:vent.append(x)
    ob.ventilator_availability = sum(vent)*100/len(vent)



