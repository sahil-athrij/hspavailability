from django.contrib import admin
from home.models import Markers, Reviews
# Register your models here.

class MarkersAdmin(admin.ModelAdmin):

    fields = ['name', 'Phone', 'size', 'financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating', 'beds_available',
              'ventilator_availability', 'oxygen_availability', 'icu_availability', 'Suspicious', 'address', 'display_address', 'location']

    search_fields = ['name']

    list_filter = ['size']

    list_display = ['name', 'Phone', 'size', 'Suspicious']

    list_editable = ['Phone']

admin.site.register(Markers, MarkersAdmin)
admin.site.register(Reviews)