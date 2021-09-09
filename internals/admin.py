from django.conf import settings
from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from internals.models import Images, Department, Department_Name, Equipment_Name, Equipment, Floors, Building, Doctor


class ImagesAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        print(obj.image)
        return format_html('<img src="{}{}" width="450" />'.format(settings.MEDIA_URL, obj.image))

    image_tag.short_description = 'Image'

    fields = ['hospital', 'review', 'image_tag', 'useinmarker']

    readonly_fields = ['hospital', 'review', 'image_tag']


admin.site.register(Images, ImagesAdmin)
admin.site.register(Department, )
admin.site.register(Department_Name, )
admin.site.register(Equipment, )
admin.site.register(Equipment_Name, )
admin.site.register(Floors, )
admin.site.register(Building, )
admin.site.register(Doctor, )
