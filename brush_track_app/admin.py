
from django.contrib import admin

from brush_track_app import  models
from brush_track_app.models import Client, Supervisor, Painter, Notification, FollowRequest, Rating
from brush_track_app.views import painters

admin.site.register(models.Login)
admin.site.register(Client)
admin.site.register(Supervisor)
admin.site.register(Painter)
admin.site.register(Notification)
admin.site.register(FollowRequest)
admin.site.register(Rating)