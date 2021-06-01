# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','maps.settings')
# import django
# django.setup()
# import requests, json
# from home.models import Markers
#
# markers = Markers.objects.all()
# for mkr in markers:
#     url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"+mkr

a = input()
odd = 0
even = 0
for i in range(0, len(a)):
    if i % 2 == 0:
        even += int(a[i])
    else:
        odd += int(a[i])
if odd == even:
    print('balance')
else:
    print('not balanced')

b = input()
h, m = b.split(':')
totalmins = 12 * 60
hmin = int(h) * 60
hangle = hmin / totalmins * 360
mangle = int(m) / 60 * 360

anglediff = abs(hangle - mangle)
if anglediff > 180:
    anglediff = 360 - anglediff
print(anglediff)

a = [int(s) for s in input().split(',')]
for i in range(len(a)):
    if a[i] == i + 1:
        break
else:
    i = -2
print(i+1)
