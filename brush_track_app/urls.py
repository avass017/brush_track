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
path('painters_view',superview.painters_view,name='painters_view'),]
