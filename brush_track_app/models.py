from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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


class Notification(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)

    supervisor = models.ForeignKey("Supervisor", on_delete=models.CASCADE)
    message= models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

class FollowRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    supervisor = models.ForeignKey("Supervisor", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

class Work(models.Model):

    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    supervisor = models.ForeignKey("Supervisor", on_delete=models.CASCADE)



    location = models.CharField(max_length=250)
    WORK_TYPE_CHOICES = [
        ("Home", "Home"),
        ("Office", "Office"),
        ("Building", "Building"),
        ("Shop", "Shop"),
        ("Apartment", "Apartment"),
    ]
    work_type = models.CharField(
        max_length=50,
        choices=WORK_TYPE_CHOICES
    )

    square_feet = models.IntegerField(null=True, blank=True)

    paint_type = models.CharField(max_length=100, null=True, blank=True)  # Interior / Exterior

    start_date = models.DateField(null=True, blank=True)

    expected_finish_date = models.DateField(null=True, blank=True)

    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Started", "Started"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.work_type

class Rating(models.Model):

    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    supervisor = models.ForeignKey("Supervisor", on_delete=models.CASCADE)

    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} rated {self.supervisor} - {self.rating}"







class WorkStatusUpdate(models.Model):
    work = models.ForeignKey("Work", on_delete=models.CASCADE, related_name="status_updates")
    status = models.CharField(max_length=100)
    progress_percentage = models.IntegerField()
    message = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.work} - {self.status} ({self.progress_percentage}%)"

class WorkAssign(models.Model):

    AREA_CHOICES = [
        ('hall', 'Hall'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('exterior', 'Exterior'),
    ]

    WORK_TYPE_CHOICES = [
        ('painting', 'Painting'),
        ('washing', 'Washing'),
        ('cleaning', 'Cleaning'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    painter = models.ForeignKey(Painter, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES)

    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.work} - {self.painter} - {self.work_type}"

class Assignment(models.Model):
    painter = models.ForeignKey(Painter, on_delete=models.CASCADE)

    work = models.ForeignKey(Work, on_delete=models.CASCADE)

class ClientMessage(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True, blank=True)
    paint_status_choices = [
        ('purchased','Purchased'),
        ('not_purchased','Not Purchased')
    ]
    paint_status = models.CharField(max_length=20, choices=paint_status_choices, default='not_purchased')
    reason = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message to {self.client} for {self.work}"