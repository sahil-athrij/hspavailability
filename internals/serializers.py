from rest_framework import serializers

from internals.models import Department, DepartmentName, Doctor, EquipmentName, \
    Floors, Building, Images, Equipment, DoctorReviews, WorkingTime, HospitalWorkingTime, \
    Nurse, Ambulance, NurseReviews, AmbulanceReviews, BloodBank, Appointment, AppointmentSlots, \
    DoctorSchedule

from django.core.exceptions import ValidationError
from django.db import IntegrityError
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
        model = DepartmentName
        fields = ['id', 'name', "icon"]


class EquipmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentName
        fields = ['id', 'name']


class GetDoctorReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="name")

    class Meta:
        model = DoctorReviews
        fields = ["content", "created_by", "doctor", "rating"]



class AppointmentSlotSerializer(serializers.ModelSerializer):
    booked = serializers.SerializerMethodField()
    class Meta:
        model = AppointmentSlots
        fields = ["id","start", "end", "booked"]
    
    def get_booked(self, AppointmentSlot):
        return False if AppointmentSlot.booked_by is None else True

    def validate(self, data):
        if(data['start'] >= data['end']):
            raise serializers.ValidationError({'start':"Start shouldn't be greater than end"})
        return data

class PatientAppointmentSlotSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(source='day.doctor.name',read_only='True')
    date = serializers.StringRelatedField(source='day.date', read_only='True')
    class Meta:
        model = AppointmentSlots
        fields = ["id","start", "end", "doctor","date"]

class DoctorScheduleSerializer(serializers.ModelSerializer):
    slots = AppointmentSlotSerializer(many=True)
    stats = serializers.SerializerMethodField()

    def create(self, validated_data):
        slots = validated_data.pop('slots')
        schedule = DoctorSchedule.objects.create(**validated_data) 
        AppointmentSlots.objects.bulk_create([AppointmentSlots(**slot,day=schedule) for slot in slots])
        return schedule

    def validate_slots(self, data):
        slot_len = len(data)
        for i in range(slot_len-1):
            for j in range(i+1,slot_len):
                if(data[i]['start'] > data[j]['end'] or data[i]['end'] < data[j]['start'] ):
                    continue
                raise serializers.ValidationError("time intersects")
        return data

    class Meta:
        model = DoctorSchedule
        fields = ["id","date","slots", "stats","doctor"]
        extra_kwargs = {
            'doctor': {'write_only':True}
        }
    def get_stats(self, doctorSchedule):
        appointments = AppointmentSlots.objects.filter(day=doctorSchedule.id)
        total = appointments.count()
        available = appointments.filter(booked_by__isnull=True).count()
        return {"total":total,"available":available} 



class DoctorSerializer(serializers.ModelSerializer):
    reviews = GetDoctorReviewSerializer(many=True, required=False, read_only=True)
    working_time = HospitalWorkingTimeSerializer(many=True, read_only=True)
    #ranges = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", 'name', 'phone_number', 'hospital', 'department', 'user', 'working_time',
                  'rating', 'patients', 'experience', 'specialization', "about", "reviews", "image", "whatsapp_number",
                  "email_id", 'ima_number']
        extra_kwargs = {
            'hospital': {'read_only': True},
            'user': {'required': False},

        }

    """def get_ranges(self, doctor):
        days = sorted(list(set([schedule.date for schedule in DoctorSchedule.objects.filter(doctor=doctor).all()])))
        ranges = []
        print(days)
        days_len = len(days)
        if days_len:
            start = days[0]

            for i in range(1, days_len):
                if ((days[i] - days[i-1]).days == 1):
                    continue
                print(start,days[i-1],days[i])
                ranges.append({"start":start,"end":days[i-1]})
                start = days[i]
            
            ranges.append({"start":start,"end":days[days_len - 1]})
            
        return ranges
    """


class EquipmentSerializer(serializers.ModelSerializer):
    name = EquipmentNameSerializer
    images = GetImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Equipment
        fields = ['name', 'images']


class GetDepartmentSerializer(serializers.ModelSerializer):
    images = GetImageSerializer(many=True, required=False, read_only=True)
    name = DepartmentNameSerializer(many=False, required=False, read_only=True)
    name_id = serializers.PrimaryKeyRelatedField(queryset=DepartmentName.objects.all(), source='name')
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
    hospital = serializers.ReadOnlyField(source="hospital.name")

    class Meta:
        model = BloodBank
        fields = [
            'name', 'phone_no', 'blood_avail_Bpos', 'blood_avail_Apos', 'blood_avail_ABpos', 'blood_avail_Opos',
            'blood_avail_Bneg', 'blood_avail_Aneg', 'blood_avail_Oneg', 'blood_avail_ABneg', 'hospital'
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
