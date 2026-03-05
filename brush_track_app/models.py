from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Login(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_painter = models.BooleanField(default=False)


class Client(models.Model):
    client_details = models.OneToOneField("Login", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField(max_length=50)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    supervisor_details = models.OneToOneField("Login", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField(max_length=50)
    document = models.FileField(upload_to='documents/')
    id_proof = models.FileField(upload_to='documents/')
    experience_years = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Painter(models.Model):
        painter_details = models.OneToOneField("Login",on_delete=models.CASCADE)

        supervisor = models.ForeignKey("Supervisor",on_delete=models.SET_NULL,null=True,related_name="painters")

        name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        phone = models.CharField(max_length=15)
        address = models.TextField()

        experience_years = models.PositiveIntegerField(default=0)
        document = models.FileField(upload_to='painter_documents/',blank=True,null=True)

        def __str__(self):
            return self.name


