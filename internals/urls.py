from django.urls import path, include
from rest_framework.routers import DefaultRouter

from internals.views import *

router = DefaultRouter()
router.register(r'doctors', DoctorApiViewSet)
router.register(r'doctor_reviews', DoctorReviewViewSet)
router.register(r'department_names', Department_NameApiViewSet)
router.register(r'departments', DepartmentApiViewSet)
router.register(r'equipment_names', Equipment_NameApiViewSet)
router.register(r'equipments', EquipmentApiViewSet)
router.register(r'floors', FloorApiViewSet)
router.register(r'buildings', BuildingApiViewSet)
router.register(r'profile', ProfilePictureViewSet)
router.register(r'nurses', NurseApiViewSet)
router.register(r'nurse_reviews', NurseReviewViewSet)
router.register(r'ambulance', AmbulanceApiViewSet)
urlpatterns = [path(r'', include(router.urls))]
