from django.contrib.auth import logout
from django.db.models import Avg
from django.shortcuts import render, redirect

from brush_track_app.forms import NotificationRegister, WorkStatusUpdateRegister, WorkAssignForm, supervisorRegister, \
    ClientMessageForm
from brush_track_app.models import Supervisor, Painter, Notification, FollowRequest, Work, Rating, Client, \
    WorkStatusUpdate, WorkAssign


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

    return render(request, 'supervisor/work_view.html', {'works': works})

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



def add_work_status_update(request, id):
    supervisor = Supervisor.objects.get(supervisor_details=request.user)
    work = Work.objects.get(id=id, supervisor=supervisor)

    if request.method == "POST":
        form = WorkStatusUpdateRegister(request.POST)
        if form.is_valid():
            status_update = form.save(commit=False)
            status_update.work = work
            status_update.save()

            if status_update.progress_percentage >= 100:
                work.status = "Completed"
            elif work.status == "Pending":
                work.status = "Started"
            work.save()

            return redirect("supervisor_works")
    else:
        form = WorkStatusUpdateRegister()

    updates = WorkStatusUpdate.objects.filter(work=work).order_by('-updated_at')

    return render(request, 'supervisor/work_status_update_add.html', {
        'form': form,
        'work': work,
        'updates': updates,
    })


def assign_painter(request, id):

    work = Work.objects.get(id=id)
    supervisor = Supervisor.objects.get(supervisor_details=request.user)

    if request.method == "POST":
        form = WorkAssignForm(request.POST)

        if form.is_valid():
            assign = form.save(commit=False)
            assign.work = work
            assign.client = work.client
            assign.supervisor = supervisor
            assign.save()

            return redirect('supervisor_works')

    else:
        form = WorkAssignForm()

    return render(request,'supervisor/assign_painter.html',{
        'form':form,
        'work':work
    })

def supervisor_assigned_works(request):

    supervisor = Supervisor.objects.get(supervisor_details=request.user)

    assigned_works = WorkAssign.objects.filter(supervisor=supervisor)

    return render(request,'supervisor/assigned_works.html',{
        'assigned_works':assigned_works
    })


def supervisor_dashboard(request):

    supervisor = Supervisor.objects.get(supervisor_details=request.user)

    painters_count = Painter.objects.filter(supervisor=supervisor).count()

    requests = FollowRequest.objects.filter(supervisor=supervisor)

    pending_requests = requests.filter(status="Pending").count()

    works = Work.objects.filter(supervisor=supervisor)

    total_works = works.count()

    completed_works = works.filter(status="Completed").count()

    assigned_works = WorkAssign.objects.filter(supervisor=supervisor)

    notifications = Notification.objects.filter(supervisor=supervisor).order_by("-date_time")[:5]

    avg_rating = Rating.objects.filter(
        supervisor=supervisor
    ).aggregate(Avg("rating"))["rating__avg"]

    context = {
        "painters_count": painters_count,
        "pending_requests": pending_requests,
        "total_works": total_works,
        "completed_works": completed_works,
        "assigned_works": assigned_works[:5],
        "notifications": notifications,
        "avg_rating": avg_rating,
    }

    return render(request,"supervisor/dashboard.html",context)

def super_update(request,id):
    pas_up=Supervisor.objects.get(id=id)

    if request.method == "POST":
        up_form = supervisorRegister(request.POST,instance=pas_up)
        if up_form.is_valid():
            up_form.save()
            return redirect('supervisor_profile')
    else:
        up_form = supervisorRegister(instance=pas_up)
    return render(request,'supervisor/supdate.html',{'data':up_form})

def send_message_to_client(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    supervisor = getattr(request.user, 'supervisor', None)

    if not client or not supervisor:
        return render(request, 'supervisor/error.html', {
            'message': 'Client or supervisor not found!'
        })

    form = ClientMessageForm(request.POST or None)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.client = client
        msg.supervisor = supervisor
        msg.save()
        return redirect('supervisor_dashboard')

    return render(request, 'supervisor/send_message.html', {'form': form, 'client': client})

def Log_out_super(request):
    logout(request)
    return redirect('login_view')