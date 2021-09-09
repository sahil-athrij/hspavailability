from rest_framework import serializers

from internals.models import Department, Department_Name, Doctor, Equipment_Name, Floors, Building, Images, Equipment


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


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'phone_number', 'hospital', 'department', 'user']
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
        fields = ['name', 'x', 'y', 'hospital', 'images', 'doctors']
        extra_kwargs = {
            'images': {'required': True},
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
