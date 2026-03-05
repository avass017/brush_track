from django.shortcuts import render

from brush_track_app.models import Painter


def painter_profile(request):
    data = request.user
    paint_prof = Painter.objects.get(painter_details=data.id)
    return render(request,"painter/profile_p.html",{'data':paint_prof})