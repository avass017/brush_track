from django.urls import path

from brush_track_app import views, clientview, superview, painterview

urlpatterns = [
path('',views.index,name='index'),
path('login_page',views.login_page,name='login_page'),
path('login_view',views.login_view,name='login_view'),
path('admin',views.admin,name='admin'),
path('client',views.client,name='client'),
path('supervisor',views.supervisor,name='supervisor'),
path('painters',views.painters,name='painters'),
path('client_add',views.client_add,name='client_add'),
path('client_profile',clientview.client_profile,name='client_profile'),
path('supervisor_add',views.supervisor_add,name ='supervisor_add'),
path('supervisor_profile',superview.supervisor_profile,name='supervisor_profile'),
path('painter_add',views.painter_add,name='painter_add'),
path('painter_profile',painterview.painter_profile,name='painter_profile'),
path('supervisor_view',clientview.supervisor_view,name='supervisor_view'),
path('painters_view',superview.painters_view,name='painters_view'),
path('notification',superview.notification,name='notification'),
path('send_notification',superview.send_notification,name='send_notification'),
path('painter_notifications',painterview.painter_notifications,name='painter_notifications'),
path('send_request/<int:id>/', clientview.send_request, name='send_request'),

path('supervisor_requests/', superview.supervisor_requests, name='supervisor_requests'),

path('accept_request/<int:id>/', superview.accept_request, name='accept_request'),

path('reject_request/<int:id>/', superview.reject_request, name='reject_request'),
path('client_requests',clientview.client_requests,name='client_requests'),
path("supervisor_works/", superview.supervisor_works, name="supervisor_works"),
path("add_work/<int:id>/", clientview.add_work, name="add_work"),
path('accept_work/<int:id>/', superview.accept_work, name="accept_work"),
path('reject_work/<int:id>/', superview.reject_work, name="reject_work"),
path('client_notifications/',clientview.client_notifications,name="client_notifications"),
path("add_rating/<int:id>/",clientview.add_rating,name="add_rating"),



]

