from django.contrib import admin
from django.utils.html import format_html
from home.models import Markers, Reviews, SuspiciousMarking, Patient, Tokens, Language, Spoken_Language
from django.conf import settings


# Register your models here.

class MarkersAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'Phone', 'size')
        }),
        ('Extra Fields', {
            'classes': ('collapse',),
            'fields': ('financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
                       'ventilator_availability', 'oxygen_availability', 'icu_availability', 'Suspicious', 'address',
                       'display_address', 'lat', 'lng', 'location')
        })
    )

    readonly_fields = ['financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
                       'ventilator_availability', 'oxygen_availability', 'icu_availability',
                       'Suspicious', 'lat', 'lng']

    search_fields = ['name']

    list_filter = ['size']

    list_display = ['name', 'id', 'Phone', 'size', 'Suspicious']

    list_editable = ['Phone']


admin.site.register(Markers, MarkersAdmin)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    raw_id_fields = ('marker',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    raw_id_fields = ('hospitalprefid',)

admin.site.register(SuspiciousMarking)

admin.site.register(Tokens)


admin.site.register(Language)
admin.site.register(Spoken_Language)



