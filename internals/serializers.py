from rest_framework import serializers

from internals.models import Department, Department_Name, Doctor, Equipment_Name, \
    Floors, Building, Images, Equipment, DoctorReviews, WorkingTime, HospitalWorkingTime, \
    Nurse, Ambulance, NurseReviews, AmbulanceReviews, Blood_bank, Appointment, AvailableSlots


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


class EquipmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment_Name
        fields = ['id', 'name']


class GetDoctorReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = DoctorReviews
        fields = ["content", "created_by", "doctor", "rating"]


class AvailableSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlots
        fields = ["date", "start", "end"]


class DoctorSerializer(serializers.ModelSerializer):
    reviews = GetDoctorReviewSerializer(many=True, required=False, read_only=True)
    working_time = HospitalWorkingTimeSerializer(many=True, read_only=True)
    slots = AvailableSlotsSerializer(many=True, read_only=True)
    ranges = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", 'name', 'phone_number', 'hospital', 'department', 'user', 'working_time',
                  'rating', 'patients', 'experience', 'specialization', "about", "reviews", "image", "whatsapp_number",
                  "email_id", 'ima_number', 'slots', 'ranges']
        extra_kwargs = {
            'hospital': {'read_only': True},
            'user': {'required': False},

        }

    def get_ranges(self, doctor):
        days = sorted(list(set([slot.date for slot in doctor.slots.all()])))
        ranges = []
        print(days)
        if len(days):
            temp = days[0]
            for i in range(1, len(days)):
                print(temp, days[i], temp.day - days[i].day)
                if temp.day - days[i].day < -2:
                    print({"start": temp, "end": days[i - 1]})
                    ranges.append({"start": temp, "end": days[i - 1]})
                    temp = days[i]

        return ranges


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
        fields = ['id', 'name', 'x', 'y', 'hospital', 'images', 'doctors', 'name_id', 'rating']
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
            'id', 'name', 'gender', 'hospital', 'experience', 'patients', 'image', 'user', 'rating', 'home_care',
            'about',
            'phone_number', 'review', 'whats_app', 'services', 'availability'
        ]


class GetNurseReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = NurseReviews
        fields = ["content", "created_by", "nurse", "rating"]


class AmbulanceSerializer(serializers.ModelSerializer):
    hospital = serializers.ReadOnlyField(source="hospital.name")

    class Meta:
        model = Ambulance
        fields = [
            'id', 'name', 'driver_name', 'hospital', 'phone_number', 'image', 'rating'
        ]


class GetAmbulanceReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = AmbulanceReviews
        fields = ["content", "created_by", "ambulance", "rating"]


class Blood_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_bank
        fields = [
            'name', 'phone_no', 'blood_avail_Bpos', 'blood_avail_Apos', 'blood_avail_ABpos', 'blood_avail_Opos',
            'blood_avail_Bneg', 'blood_avail_Aneg', 'blood_avail_Oneg', 'blood_avail_ABneg'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'doctor', 'date', 'approved', 'patient', 'start', 'end'
        ]
        extra_kwargs = {
            'approved': {'read_only': True},
        }
