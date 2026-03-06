from django.shortcuts import render, redirect

from brush_track_app.forms import WorkRegister
from brush_track_app.models import Client, Supervisor, FollowRequest, Notification


def client_profile(request):
    data = request.user
    client_prof = Client.objects.get(client_details=data.id)
    return render(request,"client/profile_c.html",{'data':client_prof})

def supervisor_view(request):

    supervisors = Supervisor.objects.all()

    client = Client.objects.get(client_details=request.user)

    requests = FollowRequest.objects.filter(client=client)

    context = {
        'data': supervisors,
        'requests': requests
    }

    return render(request,'client/super_view.html',context)
def send_request(request, id):

    supervisor = Supervisor.objects.get(id=id)
    client = Client.objects.get(client_details=request.user)

    FollowRequest.objects.create(
        client=client,
        supervisor=supervisor
    )

    return redirect('supervisor_view')

def client_requests(request):

    client = Client.objects.get(client_details=request.user)

    requests = FollowRequest.objects.filter(client=client)

    return render(request,'client/request_status.html',{'requests':requests})

def add_work(request, id):

    supervisor = Supervisor.objects.get(id=id)
    client = Client.objects.get(client_details=request.user)

    if request.method == "POST":

        form = WorkRegister(request.POST)

        if form.is_valid():

            work = form.save(commit=False)
            work.client = client
            work.supervisor = supervisor
            work.save()

            return redirect("supervisor_view")

    else:
        form = WorkRegister()

    return render(request, "client/work_add.html", {"form": form})

def client_notifications(request):

    client = Client.objects.get(client_details=request.user)

    notifications = Notification.objects.filter(client=client).order_by('-date_time')

    return render(request,'client/notifications.html',{'notifications':notifications})