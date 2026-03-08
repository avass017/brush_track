from django.shortcuts import render, redirect


from brush_track_app.models import Painter, Notification, Work


def painter_profile(request):
    data = request.user
    paint_prof = Painter.objects.get(painter_details=data.id)
    return render(request,"painter/profile_p.html",{'data':paint_prof})

def painter_notifications(request):
    # Get the painter instance for the logged-in user
    painter = getattr(request.user, 'painter', None)
    if not painter:
        return redirect('home')
    supervisor = painter.supervisor
    notifications = Notification.objects.filter(supervisor=supervisor).order_by('-date_time')

    return render(request, 'painter/super_notification.html', {'data': notifications})

