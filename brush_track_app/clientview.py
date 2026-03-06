from django.shortcuts import render, redirect

from brush_track_app.forms import WorkRegister, RatingRegister
from brush_track_app.models import Client, Supervisor, FollowRequest, Notification


def client_profile(request):
    data = request.user
    client_prof = Client.objects.get(client_details=data.id)
    return render(request,"client/profile_c.html",{'data':client_prof})

from django.db.models import Avg
from .models import Supervisor, Client, FollowRequest, Rating

def supervisor_view(request):

    supervisors = Supervisor.objects.all()

    client = Client.objects.get(client_details=request.user)

    requests = FollowRequest.objects.filter(client=client)

    # ⭐ Calculate average rating for each supervisor
    for sup in supervisors:
        sup.avg_rating = Rating.objects.filter(
            supervisor=sup
        ).aggregate(Avg("rating"))["rating__avg"]

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

def add_rating(request, id):

    supervisor = Supervisor.objects.get(id=id)
    client = Client.objects.get(client_details=request.user)

    form = RatingRegister()

    if request.method == "POST":
        form = RatingRegister(request.POST)

        if form.is_valid():

            rating = form.save(commit=False)
            rating.client = client
            rating.supervisor = supervisor
            rating.save()

            return redirect("supervisor_view")

    return render(request,"client/add_rating.html",{
        "form":form
    })