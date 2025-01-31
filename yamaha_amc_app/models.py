from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Trainer"), (3, "Customer"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=50)

    # Ensure a default username for customers if not provided
    def save(self, *args, **kwargs):
        if self.user_type == "3" and not self.username:  # If Customer and username is blank
            self.username = f"customer_{self.email.split('@')[0]}"[:150]  # Generate a default username
        super().save(*args, **kwargs)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Trainer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    price=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    unique_id=models.CharField(max_length=255, unique=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    date_of_purchase=models.DateField()
    model=models.CharField(max_length=255)
    frame_no=models.CharField(max_length=255)
    registration_no=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager() 

class customerservice(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    no_of_service=models.IntegerField()
    effective_from=models.DateField()
    effective_to=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerserviceStatement(models.Model):
    id=models.AutoField(primary_key=True)
    customerservice_id=models.ForeignKey(customerservice, on_delete=models.CASCADE, default=1)
    service_date=models.DateField()
    service_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class CustomerDue(models.Model):
    id=models.AutoField(primary_key=True)
    trainer_id=models.ForeignKey(Trainer, on_delete=models.CASCADE, default=1)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    session_start_date=models.DateField()
    session_end_date=models.DateField()
    amount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Event(models.Model):
    id=models.AutoField(primary_key=True)
    event_name=models.CharField(max_length=255)
    event_date=models.DateField()
    event_description=models.TextField()
    amount=models.CharField(max_length=255)
    total_participation=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class EventParticipation(models.Model):
    id=models.AutoField(primary_key=True)
    event_id=models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    participator=models.CharField(max_length=255)
    amount=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerLeave(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    trainer_id=models.ForeignKey(Trainer, on_delete=models.CASCADE, default=1)
    start_date=models.DateField()
    end_date=models.DateField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Messages(models.Model):
    id=models.AutoField(primary_key=True)
    end_date=models.DateField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerAgree(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Trainer.objects.create(admin=instance,address="",profile_pic="",gender="", price="", phoneno="")
        if instance.user_type==3:
            Customer.objects.create(admin=instance, unique_id="", address="",profile_pic="",gender="", date_of_purchase=date.today(), model="", frame_no=0, phoneno="", registration_no="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.trainer.save()
    if instance.user_type==3:
        instance.customer.save()
