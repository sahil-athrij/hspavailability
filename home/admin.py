from django.contrib import admin
from home.models import Markers, Reviews, SuspiciousMarking, Patient
# Register your models here.

class MarkersAdmin(admin.ModelAdmin):

    fieldsets = (
        (None,{
            'fields':('name', 'Phone', 'size')
        }),
        ('Extra Fields',{
            'classes':('collapse',),
            'fields':('financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
              'ventilator_availability', 'oxygen_availability', 'icu_availability', 'Suspicious', 'address', 'display_address','lat', 'lng', 'location')
        })
    )

    # fields = ['name', 'Phone', 'size', 'financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
    #           'ventilator_availability', 'oxygen_availability', 'icu_availability', 'Suspicious', 'address', 'display_address','lat', 'lng', 'location']

    search_fields = ['name']

    list_filter = ['size']

    list_display = ['name', 'id', 'Phone', 'size', 'Suspicious']

    list_editable = ['Phone']

admin.site.register(Markers, MarkersAdmin)
admin.site.register(Reviews)
admin.site.register(SuspiciousMarking)
admin.site.register(Patient)