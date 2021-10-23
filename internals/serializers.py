from rest_framework import serializers

from internals.models import Department, Department_Name, Doctor, Equipment_Name,\
    Floors, Building, Images, Equipment, DoctorReviews, WorkingTime, HospitalWorkingTime, Nurse, Ambulance, ProfileImage, NurseReviews


class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image', 'useinmarker', 'hospital', 'review'
        ]


class GetWorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingTime
        fields = ["day", "starting_time", "ending_time"]


class HospitalWorkingTimeSerializer(serializers.ModelSerializer):
    working_time = GetWorkingTimeSerializer(many=False)

    class Meta:
        model = HospitalWorkingTime
        fields = ["working_time", "hospital"]


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_Name
        fields = ['id', 'name', "icon"]


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['user', 'image']
        extra_kwargs = {
            'user': {'read_only': True},
        }

class EquipmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment_Name
        fields = ['id', 'name']


class GetDoctorReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = DoctorReviews
        fields = ["content", "created_by", "doctor", "rating"]


class DoctorSerializer(serializers.ModelSerializer):
    reviews = GetDoctorReviewSerializer(many=True, required=False, read_only=True)
    working_time = HospitalWorkingTimeSerializer(many=True,read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", 'name', 'phone_number', 'hospital', 'department', 'user', 'working_time',
                  'rating', 'patients', 'experience', 'specialization', "about", "reviews", "image","whatsapp_number","email_id", "language"]
        extra_kwargs = {
            'hospital': {'read_only': True},
            'user': {'required': False},

        }


class EquipmentSerializer(serializers.ModelSerializer):
    name = EquipmentNameSerializer
    images = GetImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Equipment
        fields = ['name', 'images']


class GetDepartmentSerializer(serializers.ModelSerializer):
    images = GetImageSerializer(many=True, required=False, read_only=True)
    name = DepartmentNameSerializer(many=False, required=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(queryset=Department_Name.objects.all(), source='name')
    doctors = DoctorSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Department
        fields = ['id','name', 'x', 'y', 'hospital', 'images', 'doctors', 'name_id', 'rating']
        extra_kwargs = {
            'images': {'read_only': True},
            'doctor': {'read_only': True},
        }


class GetFloorSerializer(serializers.ModelSerializer):
    departments = GetDepartmentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Floors
        fields = ['number', 'departments', 'building']


class GetBuildingSerializer(serializers.ModelSerializer):
    floors = GetFloorSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Building
        fields = ['name', 'floor_plan', 'floors']

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = [
            'id','name', 'gender', 'hospital', 'experience', 'patients', 'image', 'user','rating','home_care','about','phone_number','review'
        ]


class GetNurseReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = NurseReviews
        fields = ["content", "created_by", "nurse", "rating"]

class AmbulanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = [
            'id','name', 'driver_name', 'hospital','phone_number'
        ]

