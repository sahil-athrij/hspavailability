import django_filters
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from internals.models import *
from internals.serializers import *


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


class DepartmentApiViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = GetDepartmentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['hospital']

class EquipmentApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class FloorApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Floors.objects.all()
    serializer_class = GetFloorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class BuildingApiViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Building.objects.all()
    serializer_class = GetBuildingSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class DoctorApiViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']

    def create(self, request, *args, **kwargs):

        doctor = Doctor.objects.filter(phone_number=self.request.data["phone_number"]).first()
        if not doctor:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            doctor = serializer.save()

        print(doctor)
        working_times = self.request.data["working_time"]
        print(working_times)
        for data in working_times:

            print(f"{data = }")
            hospital = data['hospital']
            print(f"{hospital = }")
            working_time_obj, _ = WorkingTime.objects.get_or_create(day=data["working_time"].get("day"),
                                                                    starting_time=data["working_time"].get(
                                                                        "starting_time"),
                                                                    ending_time=data["working_time"].get("ending_time"))
            print(working_time_obj)
            hs = Markers.objects.get(id=hospital)
            HospitalWorkingTime.objects.create(working_time=working_time_obj,
                                               hospital=hs, doctor=doctor)
            return Response(self.serializer_class(doctor).data, status=201, )

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
# {
#   "name": "sunith",
#   "phone_number": "9961693831",
#   "department": [
#     4  ],
#   "working_time": [
#     {
#       "working_time": {
#         "day": 1,
#         "starting_time": "06:00:00",
#         "ending_time": "12:00:00"
#       },
#       "hospital": 45351
#     }
#   ]
# }