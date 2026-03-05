from django.shortcuts import render, redirect

from brush_track_app.models import Supervisor, Painter

def supervisor_profile(request):
    data = request.user
    client_prof = Supervisor.objects.get(supervisor_details=data.id)
    return render(request,"supervisor/profile_s.html",{'data':client_prof})

def painters_view(request):
    login_user = request.user

    supervisor = Supervisor.objects.get(supervisor_details=login_user)

    painters = Painter.objects.filter(supervisor=supervisor)

    return render(request, 'supervisor/painter_list.html', {'data': painters})

