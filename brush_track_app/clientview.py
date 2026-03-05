from django.shortcuts import render, redirect


from brush_track_app.models import Client, Supervisor


def client_profile(request):
    data = request.user
    client_prof = Client.objects.get(client_details=data.id)
    return render(request,"client/profile_c.html",{'data':client_prof})

def supervisor_view(request):
    data = Supervisor.objects.all()
    return render(request, 'client/super_view.html', {"data":data})

