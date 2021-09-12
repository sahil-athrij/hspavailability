from rest_framework import serializers

from internals.models import Department, Department_Name, Doctor, Equipment_Name, Floors, Building, Images, Equipment,DoctorReviews


class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image', 'useinmarker', 'hospital', 'review'
        ]


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_Name
        fields = ['id', 'name']


class EquipmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment_Name
        fields = ['id', 'name']


class GetDoctorReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = DoctorReviews
        fields = ["content", "created_by", "doctor"]


class DoctorSerializer(serializers.ModelSerializer):
    reviews = GetDoctorReviewSerializer(many=True)

    class Meta:
        model = Doctor
        fields = ["id", 'name', 'phone_number', 'hospital', 'department', 'user', 'working_time',
                  'rating', 'patients', 'experience']
        extra_kwargs = {
            'hospital': {'required': False},
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
        fields = ['name', 'x', 'y', 'hospital', 'images', 'doctors','name_id']
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
