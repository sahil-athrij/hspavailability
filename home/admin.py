from django.contrib import admin
from django.utils.html import format_html
from home.models import Markers, Reviews, SuspiciousMarking, Patient, Images, Tokens
from django.conf import settings
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

    readonly_fields = ['financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
              'ventilator_availability', 'oxygen_availability', 'icu_availability',
              'Suspicious', 'lat', 'lng']

    search_fields = ['name']

    list_filter = ['size']

    list_display = ['name', 'id', 'Phone', 'size', 'Suspicious']

    list_editable = ['Phone']

class ImagesAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        print(obj.image)
        return format_html('<img src="{}{}" width="450" />'.format(settings.MEDIA_URL,obj.image))

    image_tag.short_description = 'Image'

    fields = ['hospital', 'review','image_tag', 'useinmarker']

    readonly_fields = ['hospital', 'review', 'image_tag']

admin.site.register(Markers, MarkersAdmin)
admin.site.register(Reviews)
admin.site.register(SuspiciousMarking)
admin.site.register(Patient)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Tokens)