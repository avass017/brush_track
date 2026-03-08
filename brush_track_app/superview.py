from django.db.models import Avg
from django.shortcuts import render, redirect

from brush_track_app.forms import NotificationRegister
from brush_track_app.models import Supervisor, Painter, Notification, FollowRequest, Work, Rating,  Client


def supervisor_profile(request):
    data = request.user
    client_prof = Supervisor.objects.get(supervisor_details=data.id)
    return render(request,"supervisor/profile_s.html",{'data':client_prof})

def painters_view(request):
    login_user = request.user

    supervisor = Supervisor.objects.get(supervisor_details=login_user)

    painters = Painter.objects.filter(supervisor=supervisor)

    return render(request, 'supervisor/painter_list.html', {'data': painters})

def send_notification(request):

    form = NotificationRegister()

    if request.method == "POST":
        form = NotificationRegister(request.POST)

        if form.is_valid():

            notification = form.save(commit=False)

            supervisor = Supervisor.objects.get(supervisor_details=request.user)

            notification.supervisor = supervisor

            # assign client
            client_id = request.POST.get('client')
            notification.client = Client.objects.get(id=client_id)

            notification.save()

            return redirect('notification')

    return render(request,'supervisor/notification_add.html',{'form':form})




def notification(request):

    try:
        supervisor = Supervisor.objects.get(supervisor_details=request.user)
    except Supervisor.DoesNotExist:
        return redirect('home')

    notifications = Notification.objects.filter(
        supervisor=supervisor
    ).order_by('-date_time')

    return render(request,'supervisor/notification_view.html',{
        'data':notifications
    })

def supervisor_requests(request):

    supervisor = Supervisor.objects.get(supervisor_details=request.user)

    data = FollowRequest.objects.filter(supervisor=supervisor)

    reviews = Rating.objects.filter(supervisor=supervisor)

    avg_rating = Rating.objects.filter(
        supervisor=supervisor
    ).aggregate(Avg("rating"))["rating__avg"]

    context = {
        "data": data,
        "reviews": reviews,
        "avg_rating": avg_rating
    }

    return render(request, "supervisor/request_view.html", context)
def accept_request(request, id):

    req = FollowRequest.objects.get(id=id)
    req.status = "Accepted"
    req.save()

    return redirect('supervisor_requests')

def reject_request(request, id):

    req = FollowRequest.objects.get(id=id)
    req.status = "Rejected"
    req.save()

    return redirect('supervisor_requests')


def supervisor_works(request):

    supervisor = Supervisor.objects.get(supervisor_details=request.user)

    works = Work.objects.filter(supervisor=supervisor)

    return render(request,'supervisor/work_view.html',{'works':works})

def accept_work(request, id):

    work = Work.objects.get(id=id)
    work.status = "Accepted"
    work.save()

    Notification.objects.create(
        client=work.client,
        supervisor=work.supervisor,
        message="Your work request has been accepted by supervisor"
    )

    return redirect('supervisor_works')


def reject_work(request, id):

    work = Work.objects.get(id=id)

    work.status = "Rejected"
    work.save()

    Notification.objects.create(
        client=work.client,
        supervisor=work.supervisor,
        message="Your work request has been rejected by supervisor"
    )

    return redirect('supervisor_works')


