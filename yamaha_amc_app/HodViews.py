from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from urllib.parse import quote
from datetime import date
from django.contrib.auth.models import UserManager
import string
import random
from django.utils.crypto import get_random_string


from yamaha_amc_app.models import CustomUser, Customer, Trainer, CustomerDue, Event, EventParticipation, Messages, CustomerAgree, customerservice, CustomerserviceStatement
from yamaha_amc_app.forms import AddTrainerForm, EditTrainerForm, AddCustomerForm, EditCustomerForm, AddGymFeesForm, EditGymFeesForm, AddEventForm, EditEventForm, AddParticipationForm, AddCustomerLeaveForm, EditCustomerServiceForm

from django.core.mail import send_mail


def generate_random_password():
    return get_random_string(length=8)

def admin_home(request):
    trainers=Trainer.objects.all()
    customers=Customer.objects.all()

    trainer_count = trainers.count()
    customer_count = customers.count()

    context = {
        "trainer": trainers,
        "customer": customers,
        "count_trainer": trainer_count,
        "count_customer": customer_count,  
    }
    return render(request, "hod_template/home_content.html", {"context": context})

def add_trainer(request):
    form=AddTrainerForm()
    return render(request, "hod_template/add_staff_template.html", {"form": form})

def save_add_trainer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddTrainerForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            gender=form.cleaned_data["gender"]
            price=form.cleaned_data["price"]
            phoneno=form.cleaned_data["phoneno"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                user.trainer.address=address
                user.trainer.gender=gender
                user.trainer.price=price
                user.trainer.phoneno=phoneno
                user.trainer.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Trainer")
                return HttpResponseRedirect("/add_trainer")
            except:
                messages.error(request,"Failed to add Trainer")
                return HttpResponseRedirect("/add_trainer")
        else:
            messages.error(request,"Invalid form data")
            return HttpResponseRedirect("/add_trainer")
        
def manage_trainer(request):
    query = request.GET.get('search')
    
    if query:
        trainers = Trainer.objects.filter(
            Q(admin__first_name__icontains=query) | 
            Q(admin__last_name__icontains=query)
        ).order_by('admin__first_name', 'admin__last_name')
    else:
        trainers = Trainer.objects.all().order_by('admin__first_name', 'admin__last_name')
    
    return render(request, "hod_template/manage_staff_template.html", {"Trainer": trainers})


def edit_trainer(request, trainer_id):
    request.session['trainer_id']= trainer_id
    trainer=Trainer.objects.get(admin=trainer_id)
    form=EditTrainerForm()
    form.fields['email'].initial=trainer.admin.email
    form.fields['first_name'].initial = trainer.admin.first_name
    form.fields['last_name'].initial = trainer.admin.last_name
    form.fields['username'].initial = trainer.admin.username
    form.fields['address'].initial = trainer.address
    form.fields['phoneno'].initial = trainer.phoneno
    form.fields['price'].initial = trainer.price
    form.fields['gender'].initial = trainer.gender

    return render(request, "hod_template/edit_staff_template.html", {"form": form, "id": trainer_id, "username": trainer.admin.username})


def save_edit_trainer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        trainer_id=request.session.get("trainer_id")
        if trainer_id==None:
            return HttpResponseRedirect("/manage_trainer")
        
        form=EditTrainerForm(request.POST, request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            address=form.cleaned_data["address"]
            gender=form.cleaned_data["gender"]
            price=form.cleaned_data["price"]
            phoneno=form.cleaned_data["phoneno"]

            if request.FILES.get('profile_pic', False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None

            try:
                user=CustomUser.objects.get(id=trainer_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                trainer=Trainer.objects.get(admin=trainer_id)
                trainer.address=address
                trainer.phoneno=phoneno
                trainer.gender=gender
                trainer.price=price
                if profile_pic_url!=None:
                    trainer.profile_pic=profile_pic_url
                trainer.save()
                del request.session['trainer_id']
                messages.success(request,"Successfully Edited Trainer")
                return HttpResponseRedirect(reverse("edit_trainer",kwargs={"trainer_id":trainer_id}))
            except:
                messages.error(request,"Failed to Edit Trainer")
                return HttpResponseRedirect(reverse("edit_trainer",kwargs={"trainer_id":trainer_id}))
        else:
            form=EditTrainerForm(request.POST)
            trainer=Trainer.objects.get(admin=trainer_id)
            return render(request,"hod_template/edit_staff_template.html",{"form":form,"id":trainer_id,"username":trainer.admin.username})


def delete_trainer(request, trainer_id):
    try:
        trainer = Trainer.objects.get(admin_id=trainer_id)
        print(trainer.admin.username)
        
        customer_due = CustomerDue.objects.filter(trainer_id=trainer)

        if customer_due.exists():
            messages.error(request, "Trainer cannot be deleted as they are associated with customer dues.")
            return redirect('/manage_trainer')
        
        trainer.delete()

        customuser = get_object_or_404(CustomUser, username=trainer.admin.username)
        customuser.delete()

        messages.success(request, "Trainer successfully deleted.")
    except Trainer.DoesNotExist:
        messages.error(request, "Trainer does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete Trainer: {e}")

    return redirect('/manage_trainer')
 
def generate_unique_id():
    length = random.randint(6, 10)  # Random length between 6 and 10
    characters = string.ascii_letters + string.digits  # Uppercase, lowercase, and digits
    unique_id = ''.join(random.choices(characters, k=length))
    return unique_id

def add_customer(request):
    form=AddCustomerForm()
    return render(request, "hod_template/add_student_template.html", {"form": form})

def save_add_customer(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            phoneno = form.cleaned_data["phoneno"]
            gender = form.cleaned_data["gender"]
            date_of_purchase = form.cleaned_data["date_of_purchase"]
            model = form.cleaned_data["model"]
            frame_no = form.cleaned_data["frame_no"]
            registration_no = form.cleaned_data["registration_no"]
            profile_pic = request.FILES['profile_pic']

            session_start_date = request.POST.get("session_start_date")
            session_end_date = request.POST.get("session_end_date")

            # Generate a random username and password for the customer
            username = email.split("@")[0] + ''.join(random.choices(string.ascii_letters, k=5))
            default_password = generate_random_password()

            unique_id = generate_unique_id()

            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=default_password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3,
                )
                user.customer.unique_id = unique_id
                user.customer.address = address
                user.customer.phoneno = phoneno
                user.customer.gender = gender
                user.customer.date_of_purchase = date_of_purchase
                user.customer.model = model
                user.customer.frame_no = frame_no
                user.customer.profile_pic = profile_pic_url
                user.customer.registration_no = registration_no
                user.save()

                customerservice.objects.update_or_create(
                    customer_id=user.customer, defaults={
                    "no_of_service": 4,
                    "effective_from": session_start_date,
                    "effective_to": session_end_date
                    }
                )

                messages.success(request, "Successfully Added Gym Member")
                return HttpResponseRedirect("/add_customer")
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, "Failed to Add Gym Member")
                return HttpResponseRedirect("/add_customer")
        else:
            print(form.errors)
            messages.error(request, "Invalid Form Data")
            return HttpResponseRedirect("/add_customer")
    
        
def manage_customer(request):
    query = request.GET.get('search')
    order = request.GET.get('order')

    customer = Customer.objects.all()

    if query:
        customer = customer.filter(
            Q(admin__first_name__icontains=query) | 
            Q(admin__last_name__icontains=query)
        )

    if order:
        if order == "join-date":
            customer = customer.order_by('admin__date_joined')
        elif order == "name":
            customer = customer.order_by('admin__first_name', 'admin__last_name')
        elif order == "purchase-date":
            customer = customer.order_by('date_of_purchase')
    else:
        customer = customer.order_by('admin__first_name', 'admin__last_name')
    
    return render(request, "hod_template/manage_student_template.html", {'customer': customer})

def edit_customer(request, customer_id):
    request.session['customer_id']= customer_id
    customer=Customer.objects.get(admin=customer_id)
    form=EditCustomerForm()
    form.fields['email'].initial=customer.admin.email
    form.fields['first_name'].initial = customer.admin.first_name
    form.fields['last_name'].initial = customer.admin.last_name
    form.fields['username'].initial = customer.admin.username
    form.fields['address'].initial = customer.address
    form.fields['phoneno'].initial = customer.phoneno
    form.fields['gender'].initial = customer.gender
    form.fields['date_of_purchase'].initial = customer.date_of_purchase
    form.fields['model'].initial = customer.model
    form.fields['frame_no'].initial = customer.frame_no
    form.fields['registration_no'].initial = customer.registration_no

    return render(request, "hod_template/edit_student_template.html", {"form": form, "id": customer_id, "username": customer.admin.username})


def save_edit_customer(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        customer_id = request.session.get("customer_id")
        if customer_id is None:
            print("Customer ID not found in session")
            return HttpResponseRedirect("/manage_customer")
        
        form = EditCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]

            # Ensure a valid username for customers
            if not username:
                username = f"customer_{email.split('@')[0]}"[:150]

            address = form.cleaned_data["address"]
            phoneno = form.cleaned_data["phoneno"]
            gender = form.cleaned_data["gender"]
            date_of_purchase = form.cleaned_data["date_of_purchase"]
            model = form.cleaned_data["model"]
            frame_no = form.cleaned_data["frame_no"]
            registration_no = form.cleaned_data["registration_no"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                user = CustomUser.objects.get(id=customer_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username  # Ensure username is set correctly
                user.save()

                customer = Customer.objects.get(admin=customer_id)
                customer.address = address
                customer.phoneno = phoneno
                customer.gender = gender
                customer.date_of_purchase = date_of_purchase
                customer.model = model
                customer.frame_no = frame_no
                customer.registration_no = registration_no
                if profile_pic_url:
                    customer.profile_pic = profile_pic_url
                customer.save()

                del request.session["customer_id"]
                messages.success(request, "Successfully Edited Gym Member")
                return HttpResponseRedirect(reverse("edit_customer", kwargs={"customer_id": customer_id}))
            except:
                messages.error(request,"Failed to Edit Gym Member")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
        else:
            print(f"Form Errors: {form.errors}")
            messages.error(request, "Invalid Form Data")
            return HttpResponseRedirect(reverse("edit_customer", kwargs={"customer_id": customer_id}))


def delete_customer(request, customer_id):
    customer=Customer.objects.get(admin_id=customer_id)
    try:
        customer_due = CustomerDue.objects.filter(customer_id=customer)
        customer_due.delete()

        customer = get_object_or_404(Customer, admin_id=customer_id)
        customer.delete()

        customuser=get_object_or_404(CustomUser, username=customer.admin.username)
        customuser.delete()

        messages.success(request, "Gym Member successfully deleted.")
    except Exception as e:
        messages.error(request, "Failed to delete Gym Member: {e}")

    return redirect('/manage_customer') 

def renewal_customer(request, customer_id):
    customer=Customer.objects.get(admin_id=customer_id)
    session_start_date=date.today()
    session_end_date = date(session_start_date.year + 1, session_start_date.month, session_start_date.day)
    try:
        customerservice.objects.update_or_create(
            customer_id=customer, defaults={
                "no_of_service": 4,
                "effective_from": session_start_date,
                "effective_to": session_end_date
            }
        )
        messages.success(request, "Gym Member successfully Renewed")
    except Exception as e:
        messages.error(request, "Failed to Renewed Gym Member: {e}")
    return redirect('/manage_customer') 

def add_gymfees(request):
    form=AddGymFeesForm()
    return render(request, "hod_template/add_gymfees_template.html", {"form": form})

def save_add_gymfees(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddGymFeesForm(request.POST)
        if form.is_valid():
            trainer = form.cleaned_data["trainer"]
            customer = form.cleaned_data["customer"]
            session_start_date = request.POST.get("session_start_date")
            amount = request.POST.get("amount")
            session_end_date = request.POST.get("session_end_date")

            try:
                trainer_id = Trainer.objects.get(id=trainer)
                customer_id = Customer.objects.get(id=customer)

                customerdue, created = CustomerDue.objects.update_or_create(
                    customer_id=customer_id,
                    defaults={
                        "trainer_id": trainer_id,
                        "session_start_date": session_start_date,
                        "amount": amount,
                        "session_end_date": session_end_date
                    }
                )

                if created:
                    messages.success(request, "Successfully Added Gym Fees")
                else:
                    messages.success(request, "Successfully Updated Gym Fees")

                return HttpResponseRedirect("/add_gymfees")
            except Exception as e:
                messages.error(request, f"Failed to Add Gym Fees: {e}")
                return HttpResponseRedirect("/add_gymfees")



def manage_gymfees(request):
    query = request.GET.get('search')
    order=request.GET.get('order')
    
    customerdue = CustomerDue.objects.all()
    if query:
        customerdue = CustomerDue.objects.filter(
            Q(customer_id__admin__first_name__icontains=query) | 
            Q(customer_id__admin__last_name__icontains=query) |
            Q(trainer_id__admin__first_name__icontains=query) |
            Q(trainer_id__admin__last_name__icontains=query)
        ).order_by('customer_id__admin__first_name', 'customer_id__admin__last_name', 'trainer_id__admin__first_name', 'trainer_id__admin__last_name')
    elif order:
        if order == "days-left":
            customerdue = customerdue.order_by('session_end_date')
        elif order == "name":
            customerdue = customerdue.order_by('customer_id__admin__first_name', 'customer_id__admin__last_name')
        elif order == "amount":
            customerdue = customerdue.order_by('-amount')
        elif order == "updated-at":
            customerdue = customerdue.order_by('-updated_at')
    else:
        customerdue=CustomerDue.objects.all().order_by('session_end_date')
    return render(request, "hod_template/manage_gymfees_template.html",{'customerdue':customerdue})

def edit_gymfees(request, customerdue_id):
    request.session['customerdue_id']= customerdue_id
    customerdue=CustomerDue.objects.get(id=customerdue_id)
    form=EditGymFeesForm()
    form.fields['trainer'].initial=customerdue.trainer_id.id
    form.fields['customer'].initial = customerdue.customer_id.id
    form.fields['session_start_date'].initial = customerdue.session_start_date
    form.fields['session_end_date'].initial = customerdue.session_end_date
    form.fields['amount'].initial = customerdue.amount
    return render(request, "hod_template/edit_gymfees_template.html", {"form": form, "id": customerdue_id, "username": customerdue.customer_id.admin.first_name})


def save_edit_gymfees(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        customerdue_id=request.session.get("customerdue_id")
        if customerdue_id==None:
            return HttpResponseRedirect("/manage_gymfees")
        
        form=EditGymFeesForm(request.POST)
        if form.is_valid():
            trainer=form.cleaned_data["trainer"]
            customer=form.cleaned_data["customer"]
            session_start_date=form.cleaned_data["session_start_date"]
            amount=form.cleaned_data["amount"]
            session_end_date=form.cleaned_data["session_end_date"]

            try:
                customerdue=CustomerDue.objects.get(id=customerdue_id)
                trainer_id=Trainer.objects.get(id=trainer)
                customer_id=Customer.objects.get(id=customer)
                customerdue.trainer_id=trainer_id
                customerdue.customer_id=customer_id
                customerdue.session_start_date=session_start_date
                customerdue.amount=amount
                customerdue.session_end_date=session_end_date
                customerdue.save()
                del request.session['customerdue_id']
                messages.success(request,"Successfully Edited Gym Fees")
                return HttpResponseRedirect(reverse("edit_gymfees",kwargs={"customerdue_id":customerdue_id}))
            except:
                messages.error(request,"Failed to Edit Gym Fees")
                return HttpResponseRedirect(reverse("edit_gymfees",kwargs={"customerdue_id":customerdue_id}))
            

def delete_gymfees(request, customerdue_id):
    try:
        customerdue = get_object_or_404(CustomerDue, id=customerdue_id)
        customerdue.delete()
        messages.success(request, "Gym Fees successfully deleted.")
    except Exception as e:
        messages.error(request, f"Failed to delete Gym Fees: {e}")

    return redirect('/manage_gymfees')

def send_gymfees(request, customerdue_id):
    try:
        customerdue = CustomerDue.objects.get(id=customerdue_id)
        customer_email = customerdue.customer_id.admin.email
        subject = "Reminder for Payment in Evergreen Gym Fitness"
        body = f"""Dear {customerdue.customer_id.admin.first_name} {customerdue.customer_id.admin.last_name},

        This is a gentle reminder for your pending payment in Evergreen Gym Fitness. The final due date for your payment was {customerdue.session_end_date}. Kindly make the payment as soon as possible.

        Best regards,
        Evergreen Gym Fitness"""

        send_mail(
            subject=subject,
            message=body,
            from_email=None,  
            recipient_list=[customer_email],
            fail_silently=False,
        )
        messages.success(request, "Reminder email sent successfully.")
        
    except CustomerDue.DoesNotExist:
        messages.error(request, "Failed to find the Customer Due.")
        
    except Exception as e:
        print(str(e))
        messages.error(request, "Failed to send email.")

    return redirect("/manage_gymfees")


def add_event(request):
    form=AddEventForm()
    return render(request, "hod_template/add_event_template.html", {"form": form})

def save_add_event(request):
    if request.method!= "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddEventForm(request.POST)
        if form.is_valid():
            eventname = form.cleaned_data["eventname"]
            eventdate = form.cleaned_data["eventdate"]
            eventdesc = form.cleaned_data["eventdesc"]
            amount = form.cleaned_data["amount"]
            try:
                Event.objects.create(event_name=eventname, event_date=eventdate, event_description=eventdesc, amount=amount,)
                messages.success(request, "Successfully Added Event")
                return HttpResponseRedirect("/add_event")
            
            except:
                messages.error(request, "Failed to Add Event")
                return HttpResponseRedirect("/add_event")
        else:
            messages.error(request,"Invalid Form Data")
            return HttpResponseRedirect("/add_event")
        
def manage_event(request):
    event=Event.objects.all()
    form = AddParticipationForm()
    eventparticipation = EventParticipation.objects.all().order_by('participator')
    return render(request,"hod_template/manage_event_template.html",{"event":event, "form":form, "eventparticipation":eventparticipation})
        
def edit_event(request, event_id):
    request.session['event_id']= event_id
    event=Event.objects.get(id=event_id)
    form=EditEventForm()
    form.fields['eventname'].initial = event.event_name
    form.fields['eventdesc'].initial = event.event_description
    form.fields['eventdate'].initial = event.event_date
    form.fields['amount'].initial = event.amount

    return render(request, "hod_template/edit_event_template.html", {"form": form, "id": event_id, "name": event.event_name})


def save_edit_event(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        event_id=request.session.get("event_id")
        if event_id==None:
            return HttpResponseRedirect("/manage_event")
        
        form=EditEventForm(request.POST)
        if form.is_valid():
            eventname = form.cleaned_data["eventname"]
            eventdate = form.cleaned_data["eventdate"]
            eventdesc = form.cleaned_data["eventdesc"]
            amount = form.cleaned_data["amount"]

            try:
                event=Event.objects.get(id=event_id)
                event.event_name=eventname
                event.event_description=eventdesc
                event.event_date=eventdate
                event.amount=amount
                event.save()

                del request.session['event_id']
                messages.success(request,"Successfully Edited Event")
                return HttpResponseRedirect(reverse("edit_event",kwargs={"event_id":event_id}))
            except:
                messages.error(request,"Failed to Edit Event")
                return HttpResponseRedirect(reverse("edit_event",kwargs={"event_id":event_id}))
        else:
            form=EditEventForm(request.POST)
            event=Event.objects.get(id=event_id)
            return render(request,"hod_template/edit_event_template.html",{"form":form,"id":event_id,"name":event.event_name})


def delete_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, "Event successfully deleted.")
    except Exception as e:
        messages.error(request, f"Failed to delete Event: {e}")

    return redirect('/manage_event')


def send_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        customers = Customer.objects.all()
        trainers = Trainer.objects.all()

        customer_emails = [customer.admin.email for customer in customers]
        trainer_emails = [trainer.admin.email for trainer in trainers]
        
        all_emails = customer_emails + trainer_emails

        subject = quote(event.event_name)
        body = f"""Dear All,

        We are excited to inform you about the upcoming event: {event.event_name} on {event.event_date}.
        
        Best regards,
        Evergreen Gym Fitness"""
        

        send_mail(
            subject=subject,
            message=body,
            from_email=None,  
            recipient_list=all_emails,
            fail_silently=False,
        )
        messages.success(request, "Reminder email sent successfully.")
        
    except Exception as e:
        print(str(e))
        messages.error(request, "Failed to send email.")
    return redirect("/manage_event")



def add_participation(request):
    form = AddParticipationForm()
    events = Event.objects.all()
    event_data = [{"id": event.id, "amount": event.amount} for event in events]
    
    return render(request, "hod_template/add_participation_template.html", {
        "form": form,
        "event_data": event_data,
    })

def save_add_participation(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddParticipationForm(request.POST)
        if form.is_valid():
            event = request.POST.get("event_id")
            participators = form.cleaned_data["participator"]
            amount = request.POST.get("amount")
            print(amount)

            try:
                event_id = Event.objects.get(id=event)
                
                for participator in participators:
                    if participator.startswith("trainer_"):
                        _, first_name, last_name = participator.split("_")
                        # Fetch trainer
                        trainer_instance = Trainer.objects.get(
                            admin__first_name=first_name,
                            admin__last_name=last_name
                        )
                        EventParticipation.objects.update_or_create(
                            event_id=event_id,
                            participator=trainer_instance.admin.first_name+" "+trainer_instance.admin.last_name,  
                            amount=amount
                        )
                    elif participator.startswith("customer_"):
                        _, first_name, last_name = participator.split("_")
                        customer_instance = Customer.objects.get(
                            admin__first_name=first_name,
                            admin__last_name=last_name
                        )
                        EventParticipation.objects.update_or_create(
                            event_id=event_id,
                            participator=customer_instance.admin.first_name+" "+customer_instance.admin.last_name, 
                            amount=amount
                        )

                messages.success(request, "Successfully Added Participation")
                return HttpResponseRedirect("/manage_event")
            except Exception as e:
                print(e)  
                messages.error(request, "Failed to Add Participation")
                return HttpResponseRedirect("/manage_event")
        else:
            messages.error(request, "Invalid Form Data")
            return HttpResponseRedirect("/manage_event")

        

def manage_participation(request, event_id):
    eventparticipation=EventParticipation.objects.filter(event_id=event_id).order_by('participator')
    return render(request, "hod_template/manage_participation_template.html",{'eventparticipation':eventparticipation})


def delete_eventparticipators(request, eventparticipation_id):
    eventparticipation = EventParticipation.objects.get(id=eventparticipation_id)
    event_id = eventparticipation.event_id.id
    eventparticipations=EventParticipation.objects.filter(event_id=event_id).order_by('participator')
    try:
        eventparticipation.delete()
        messages.success(request, f"Participator for Event have been successfully deleted.")
    except EventParticipation.DoesNotExist:
        messages.error(request, f"No participator found for this Event.")
    return render(request, "hod_template/manage_participation_template.html", {'eventparticipation':eventparticipations})


def save_add_message(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        description = request.POST.get("description")
        end_date = request.POST.get("end_date")

        try:
            # Check if any message already exists
            message = Messages.objects.first()

            if message:
                # Update the existing message
                message.description = description
                message.end_date = end_date
                message.save()
                messages.success(request, "Successfully Updated Message")
            else:
                # Create a new message if none exists
                Messages.objects.create(
                    description=description,
                    end_date=end_date
                )
                messages.success(request, "Successfully Added Message")

            return HttpResponseRedirect("/message")

        except Exception as e:
            # Handle any errors
            print(e)  # For debugging
            messages.error(request, "Failed to Add or Update Message")
            return HttpResponseRedirect("/message")

def customer_agree(request, unique_id):
    customer = Customer.objects.get(unique_id=unique_id)
    CustomerService=customerservice.objects.get(customer_id=customer.id)
    return render(request, "hod_template/customer_agree.html", {"customer": customer, "customerservice": CustomerService})

def save_customer_agree(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        customer_uniqueid = request.POST.get("customer_id")
        try:
            customer = Customer.objects.get(unique_id=customer_uniqueid)
            print(customer)
            CustomerAgree.objects.update_or_create(
                customer_id=customer
            )
            
            messages.success(request, "Successfully serviced")
            return HttpResponseRedirect("/customer_complete")
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found")
            return HttpResponseRedirect("/customer_agree")
        except Exception as e:
            print(e)
            messages.error(request, "Failed to service")
            customer = Customer.objects.get(id=customer_uniqueid)
            return render(request, "hod_template/customer_agree.html", {"customer": customer})


def customer_complete(request):
    return render(request, "hod_template/customer_complete.html" )

def customer_urldetails(request):
    customer = CustomerAgree.objects.all()
    return render(request, "hod_template/customer_urldetails.html", {"customer": customer})

def delete_customeragree(request, customeragree_id):
    customer = CustomerAgree.objects.all()
    customeragree = CustomerAgree.objects.get(id=customeragree_id)
    try:
        customeragree.delete()
        messages.success(request, f"Customer Agreement for Bike  has been successfully deleted.")
    except CustomerAgree.DoesNotExist:
        messages.error(request, f"No Customer Agreement found.")
    return render(request, "hod_template/customer_urldetails.html", {"customer": customer})

def customer_served(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        customer_id = request.POST.get("customer_id")
        description=request.POST.get("description")
        customer = CustomerAgree.objects.all()
        try:
            CustomerService=customerservice.objects.get(customer_id=customer_id)
            CustomerService.no_of_service-=1
            CustomerService.save()
            try:
                customeragree = CustomerAgree.objects.get(customer_id=customer_id)
                customeragree.delete()
            except EventParticipation.DoesNotExist:
                messages.error(request, f"No Customer Agreed ")
            try:
                CustomerserviceStatement.objects.create(
                    customerservice_id=CustomerService, service_date=date.today(), service_description=description
                )
            except:
                print(f"Error: {e}")
                messages.error(request, "Failed to Create Service Statement")

            try:
                customer_email = CustomerService.customer_id.admin.email
                subject = "Reminder for Payment in Evergreen Gym Fitness"
                body = f"""Dear {CustomerService.customer_id.admin.first_name} {CustomerService.customer_id.admin.last_name},

                This message is from Yamaha Showroom to say that you have served your bike now the remaining bike servicing is{CustomerService.no_of_service}. 

                Best regards,
                Yamaha Showroom"""

                send_mail(
                    subject=subject,
                    message=body,
                    from_email=None,  
                    recipient_list=[customer_email],
                    fail_silently=False,
                )
                
            except customerservice.DoesNotExist:
                messages.error(request, "Failed to find the Customer Service.")
                
            except Exception as e:
                print(str(e))
                messages.error(request, "Failed to send email.")

            messages.success(request,"Successfully Bike Serviced")
            return render(request, "hod_template/customer_urldetails.html", {"customer": customer})

        except Exception as e:
            print(f"Error: {e}") 
            messages.error(request,"Failed to Service Bike")
            return render(request, "hod_template/customer_urldetails.html", {"customer": customer})
    
def customer_service(request):
    query = request.GET.get('search')
    order = request.GET.get('order')

    customer = customerservice.objects.all()
    
    if query:
        customer = customer.filter(
            Q(customer_id__admin__first_name__icontains=query) | 
            Q(customer_id__admin__last_name__icontains=query)
        )
    print(customer.exists())

    if order:
        if order == "no-of-service":
            customer = customer.order_by('no_of_service')
        elif order == "name":
            customer = customer.order_by('customer_id__admin__first_name', 'customer_id__admin__last_name')
    else:
        customer = customer.order_by('customer_id__admin__first_name', 'customer_id__admin__last_name')

    return render(request, "hod_template/manage_customer_service.html", {"customer": customer})


def customer_service_statement(request, customerservice_id):
    print(customerservice_id)
    CustomerService=customerservice.objects.get(id=customerservice_id)
    print(CustomerService)
    customer_service_statement=CustomerserviceStatement.objects.filter(customerservice_id=CustomerService)
    return render(request, "hod_template/manage_customerservice_statement.html", {"customer_service_statement": customer_service_statement})


def edit_customer_service(request, customerservice_id):

    request.session['customerservice_id']= customerservice_id
    CustomerService=customerservice.objects.get(id=customerservice_id)
    form=EditCustomerServiceForm()
    form.fields['no_of_service'].initial=CustomerService.no_of_service
    form.fields['customer'].initial = CustomerService.customer_id.id
    return render(request, "hod_template/edit_customer_service.html", {"form": form, "id": customerservice_id})

def save_edit_customer_service(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        customerservice_id=request.session.get("customerservice_id")
        print("customer_service_id", customerservice_id)
        if customerservice_id==None:
            return HttpResponseRedirect("/customer_service")
        
        form=EditCustomerServiceForm(request.POST)
        if form.is_valid():
            customer=form.cleaned_data["customer"]
            print(customer)
            customer_id=Customer.objects.get(id=customer)
            print(customer_id)
            no_of_service=form.cleaned_data["no_of_service"]

            try:
                CustomerService=customerservice.objects.get(id=customerservice_id)
                customer_id=Customer.objects.get(id=customer)
                CustomerService.customer_id=customer_id
                CustomerService.no_of_service=no_of_service
                CustomerService.save()
                del request.session['customerservice_id']
                messages.success(request,"Successfully Edited Service")
                return HttpResponseRedirect(reverse("edit_customer_service",kwargs={"customerservice_id":customerservice_id}))
            except:
                messages.error(request,"Failed to Edit Service")
                return HttpResponseRedirect(reverse("edit_customer_service",kwargs={"customerservice_id":customerservice_id}))