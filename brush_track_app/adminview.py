from django.shortcuts import render, redirect

from brush_track_app.models import Client, Supervisor


def client_view(request):
    data = Client.objects.all()
    return render(request, 'admin/client.html', {"data":data})

def supervisors_view(request):
    data = Supervisor.objects.all()
    return render(request, 'admin/super.html', {"data":data})

def client_delete(request,id):
    cli_del=Client.objects.get(id=id)
    cli_del.delete()
    return redirect('client_view')

def super_delete(request,id):
    sup_del=Supervisor.objects.get(id=id)
    sup_del.delete()
    return redirect('supervisors_view')