import django_filters
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from internals.models import Department_Name, Department, Building, Equipment_Name, Equipment, Doctor, Floors
from internals.serializers import DepartmentNameSerializer, GetDepartmentSerializer, GetBuildingSerializer, \
    EquipmentNameSerializer, EquipmentSerializer, DoctorSerializer


class Department_NameApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Department_Name.objects.all()
    serializer_class = DepartmentNameSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class Equipment_NameApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Equipment_Name.objects.all()
    serializer_class = EquipmentNameSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class DepartmentApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = GetDepartmentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class EquipmentApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class FloorApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Floors.objects.all()
    serializer_class = GetDepartmentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class BuildingApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Building.objects.all()
    serializer_class = GetBuildingSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class DoctorApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
