from django.conf import settings
from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from internals.models import *


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    # def image_tag(self, obj):
    #     print(obj.image)
    #     return format_html('<img src="{}{}" width="450" />'.format(settings.MEDIA_URL, obj.image))
    #
    # image_tag.short_description = 'Image'
    # #
    fields = ['hospital', 'review', 'image', 'department', 'useinmarker', 'equipment', 'user']
    raw_id_fields = ('hospital', 'review')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ('name', 'x', 'y', 'hospital', "rating")
    raw_id_fields = ('hospital',)


@admin.register(Building)
class DepartmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('hospital',)


@admin.register(WorkingTime)
class WorkingTimeAdmin(admin.ModelAdmin):
    pass


class HospitalWorkingTimeAdmin(admin.TabularInline):
    model = HospitalWorkingTime
    raw_id_fields = ('hospital',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    inlines = (HospitalWorkingTimeAdmin,)
@admin.register(Ambulance)
class DepartmentAdmin(admin.ModelAdmin):

    raw_id_fields = ('hospital',)

admin.site.register(Department_Name, )
admin.site.register(Equipment, )
admin.site.register(Equipment_Name, )
admin.site.register(Floors, )
admin.site.register(Nurse, )
admin.site.register(NurseReviews, )
admin.site.register(DoctorReviews, )
admin.site.register(AvailableSlots, )
