from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from brush_track_app.forms import clientRegister, LoginRegister, supervisorRegister, painterRegister


def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request,'login_page.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('admin')

            elif user.is_client:
                return redirect('client_dashboard')

            elif user.is_supervisor:
                return redirect('supervisor_dashboard')

            elif user.is_painter:
                return redirect('painter_profile')


        else:
            messages.info(request, 'Invalid')
    return render(request, 'login_page.html')

def admin(request):
    return render(request,'admin/admin.html')

def client(request):
    return render(request,'client/client.html')

def supervisor(request):
    return render(request,'supervisor/super.html')

def painters(request):
    return render(request,'painter/painter.html')


def client_add(request):
    if request.method == "POST":
        cli_form = clientRegister(request.POST, request.FILES)
        login_form = LoginRegister(request.POST)

        if cli_form.is_valid() and login_form.is_valid():
            cli = login_form.save(commit=False)
            cli.is_client = True
            cli.save()

            user = cli_form.save(commit=False)
            user.client_details = cli
            user.save()


    else:
            cli_form = clientRegister()
            login_form = LoginRegister()

    return render(request,'client/client_register.html', {'cli_form': cli_form, 'login_form': login_form})


def supervisor_add(request):
    if request.method == "POST":
        sup_form = supervisorRegister(request.POST, request.FILES)
        login_form = LoginRegister(request.POST)

        if sup_form.is_valid() and login_form.is_valid():
            sup = login_form.save(commit=False)
            sup.is_supervisor = True
            sup.save()

            user = sup_form.save(commit=False)
            user.supervisor_details = sup
            user.save()


    else:
            sup_form = supervisorRegister()
            login_form = LoginRegister()

    return render(request,'supervisor/sup_register.html', {'sup_form': sup_form, 'login_form': login_form})

def painter_add(request):
    if request.method == "POST":
        pain_form = painterRegister(request.POST, request.FILES)
        login_form = LoginRegister(request.POST)

        if pain_form.is_valid() and login_form.is_valid():
            pain = login_form.save(commit=False)
            pain.is_painter = True
            pain.save()

            user = pain_form.save(commit=False)
            user.painter_details = pain
            user.save()


    else:
            pain_form = painterRegister()
            login_form = LoginRegister()

    return render(request,'painter/paint_register.html', {'pain_form': pain_form, 'login_form': login_form})
