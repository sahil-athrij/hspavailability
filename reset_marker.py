from home.views import update_marker
from home.models import Markers

markers = Markers.object.all()
for marker in markers:
    update_marker(marker.id)
    print(marker.id)