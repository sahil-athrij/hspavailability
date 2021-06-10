import json

import django_filters
import requests
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializer import *


# Create your views here.
def index(request):
    return render(request, template_name='home/index.html')


def modify(request):
    return render(request, template_name='home/forms.html')


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
    denb = []
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
        care.append(d * x.care_rating)
        if x.beds_available != 0:
            bed.append(d * (x.beds_available - 1))
            denb.append(d)
        if x.oxygen_rating != 0:
            oxy.append(d * x.oxygen_rating)
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
    ob.care_rating = round(sum(care) / dens, 1)
    ob.oxygen_rating = round(sum(oxy) / sum(deno), 1) if deno else 0
    ob.beds_available = round(sum(bed) * 100 / sum(denb), 2) if denb else 0
    ob.ventilator_availability = round(sum(vent) * 100 / sum(denv), 2) if denv else 0
    ob.oxygen_availability = round(sum(oxya) * 100 / sum(denoa), 2) if denoa else 0
    ob.icu_availability = round(sum(icu) * 100 / sum(deni), 2) if deni else 0
    ob.save()


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


class LimitOffsetPaginationWithMaxLimit(LimitOffsetPagination):
    max_limit = 100


class MarkerApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Markers.objects.all().order_by('id')
    serializer_class = getMarkerSerializer
    # http_method_names = '__all__'
    page_size = 100
    max_page_size = 100
    max_limit = 100
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = {'financial_rating': ['gte', 'lte', 'exact'],
                        'oxygen_rating': ['gte', 'lte', 'exact'], 'ventilator_availability': ['gte', 'lte', 'exact'],
                        'oxygen_availability': ['gte', 'lte', 'exact'], 'icu_availability': ['gte', 'lte', 'exact'],
                        'avg_cost': ['gte', 'lte', 'exact'],
                        'care_rating': ['gte', 'lte', 'exact'], 'covid_rating': ['gte', 'lte', 'exact'],
                        'beds_available': ['gte', 'lte', 'exact']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition = False

    def perform_create(self, serializer):
        print(self.request.data)
        user = self.request.user
        loc = Point(float(self.request.data['lat']), float(self.request.data['lng']), srid=4326)
        url = 'https://eu1.locationiq.com/v1/reverse.php?key=pk.959200a41370341f608a91b67be6e8eb&lat=' + \
              self.request.data['lat'] + '&lon=' + self.request.data['lng'] + '&format=json'
        det = requests.get(url)
        if det.status_code == 200:
            data = json.loads(det.content.decode())
            serializer.save(address=data["address"], display_address=data["display_name"], added_by=user, location=loc)
        else:
            raise serializers.ValidationError({"detail": "Address not obtainable from Latitude and Longitude"})

    def get_pagination_class(self):
        if self.condition:
            return LimitOffsetPaginationWithMaxLimit
        return PageNumberPagination

    pagination_class = property(fget=get_pagination_class)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.condition = request._request.GET.get('limit', False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        distance = float(self.request.GET.get('distance', 10000000))
        queryset = super(MarkerApiViewSet, self).filter_queryset(queryset)
        lat = float(self.request.GET.get('lat', 0))
        lng = float(self.request.GET.get('lng', 0))
        if lat and lng:
            loc = Point(lat, lng, srid=4326)
            queryset = queryset.filter(
                                       lat__gte=lat - 2.5,
                                       lat__lte=lat + 2.5,
                                       lng__gte=lng - 2.5,
                                       lng__lte=lng + 2.5,
                                       )
            queryset = queryset.filter(location__distance_lte=(loc, D(m=distance))).annotate(
                distance=Distance('location', loc)).order_by('distance')
        #   print(len(queryset.filter(location__distance_lte=(loc, D(m=distance)))))
        return queryset


class ReviewViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Reviews.objects.all()
    serializer_class = getReviewSerializer

    def perform_create(self, serializer):
        user = self.request.user
        print(self.request.data)
        rev = Reviews.objects.filter(marker=self.request.data['marker'], written_by=self.request.user).exists()
        print(rev)
        if rev:
            raise serializers.ValidationError({"detail": "Only One Review Allowed Per Hospital"})
        serializer.save(written_by=user)

    def create(self, request, *args, **kwargs):
        response = viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        mob = Markers.objects.get(id=response.data['marker'])
        rev = Reviews.objects.get(id=response.data['id'])
        rev.day = (rev.datef - mob.datef).days
        update_marker(response.data['marker'])
        return response


class SusViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    queryset = SuspiciousMarking.objects.all()
    serializer_class = getSusSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
