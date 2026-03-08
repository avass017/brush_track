from django.shortcuts import render

from brush_track_app.models import Client


def client_view(request):
    data = Client.objects.all()
    return render(request, 'admin/client.html', {"data":data})