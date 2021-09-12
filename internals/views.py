import django_filters
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from internals.models import Department_Name, Department, Building, Equipment_Name, Equipment, Doctor, Floors,DoctorReviews
from internals.serializers import DepartmentNameSerializer, GetDepartmentSerializer, GetBuildingSerializer, \
    EquipmentNameSerializer, EquipmentSerializer, DoctorSerializer,GetDoctorReviewSerializer


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


class DoctorReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = DoctorReviews.objects.all()
    serializer_class = GetDoctorReviewSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def perform_create(self, serializer):
        user = self.request.user
        doctor = self.request.data["doctor"]
        rev = DoctorReviews.objects.filter(created_by=user, doctor=doctor).exists()
        print(rev)
        if rev:
            raise serializer.ValidationError({"detail": "Only One Review Allowed Per Doctor"})
        serializer.save(created_by=user)
