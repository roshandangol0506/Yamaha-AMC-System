from django import forms
from django.forms import ChoiceField
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple, CheckboxInput

from yamaha_amc_app.models import Trainer, Customer, Event, EventParticipation 

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass


class AddTrainerForm(forms.Form):
    email=forms.EmailField(label="email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="first_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="last_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phoneno=forms.CharField(label="Phone No",max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

    price=forms.IntegerField(label="price",widget=forms.NumberInput(attrs={"class":"form-control"}), min_value=0)

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    gender=forms.ChoiceField(label="gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="profile_pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control", "accept": ".jpg, .jpeg, .png"}))



class EditTrainerForm(forms.Form):
    email=forms.EmailField(label="email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="first_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="ast_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phoneno=forms.CharField(label="Phone No",max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

    price=forms.IntegerField(label="price",widget=forms.NumberInput(attrs={"class":"form-control"}), min_value=0)

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    gender=forms.ChoiceField(label="gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="profile_pic",max_length=50,required=False,widget=forms.FileInput(attrs={"class":"form-control", "accept": ".jpg, .jpeg, .png"}))


class AddCustomerForm(forms.Form):
    email=forms.EmailField(label="email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    first_name=forms.CharField(label="first_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="last_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phoneno=forms.CharField(label="Phone No",max_length=10,widget=forms.NumberInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    gender=forms.ChoiceField(label="gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="profile_pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control", "accept": ".jpg, .jpeg, .png"}))
    date_of_purchase = forms.DateField(label="Date of Purchase", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    model = forms.CharField(label="Model",max_length=255,widget=forms.TextInput(attrs={"class": "form-control"}))
    frame_no = forms.CharField(label="Frame No",max_length=255,widget=forms.TextInput(attrs={"class": "form-control"}))
    registration_no = forms.CharField(label="Registration No.",max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))

class EditCustomerForm(forms.Form):
    email=forms.EmailField(label="email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    first_name=forms.CharField(label="first_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="last_name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phoneno=forms.CharField(label="Phone No",max_length=10,widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    gender=forms.ChoiceField(label="gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="profile_pic",max_length=50,required=False,widget=forms.FileInput(attrs={"class":"form-control", "accept": ".jpg, .jpeg, .png"}))
    date_of_purchase = forms.DateField(label="Date of Purchase", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    model = forms.CharField(label="Model",max_length=255,widget=forms.TextInput(attrs={"class": "form-control"}))
    frame_no = forms.CharField(label="Frame No",max_length=255,widget=forms.TextInput(attrs={"class": "form-control"}))
    registration_no = forms.CharField(label="Registration No.",max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))

class AddGymFeesForm(forms.Form):
    trainer = forms.ChoiceField(label="trainer", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    customer = forms.ChoiceField(label="customer", choices=[], widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(AddGymFeesForm, self).__init__(*args, **kwargs)

        trainer_list = []
        try:
            trainers = Trainer.objects.all()
            for trainer in trainers:
                small_trainer = (trainer.id, f"{trainer.admin.first_name} {trainer.admin.last_name} = {trainer.price}")
                trainer_list.append(small_trainer)
        except Trainer.DoesNotExist:
            trainer_list = []

        self.fields['trainer'].choices = trainer_list

        customer_list = []
        try:
            customers = Customer.objects.all()
            for customer in customers:
                small_customer = (customer.id, f"{customer.admin.first_name} {customer.admin.last_name}")
                customer_list.append(small_customer)
        except Customer.DoesNotExist:
            customer_list = []

        self.fields['customer'].choices = customer_list



class EditGymFeesForm(forms.Form):
    trainer_list=[]
    try:
        trainer=Trainer.objects.all()
        for trainer in trainer:
            small_trainer=(trainer.id, str(trainer.admin.first_name) +"  "+str(trainer.admin.last_name) +"   =  "+str(trainer.price))
            trainer_list.append(small_trainer)
    except:
        trainer_list=[]
    trainer=forms.ChoiceField(label="trainer",choices=trainer_list,widget=forms.Select(attrs={"class":"form-control"}))


    customer_list=[]
    try:
        customer=Customer.objects.all()
        for customer in customer:
            small_customer=(customer.id,str(customer.admin.first_name) +"  "+str(customer.admin.last_name)) 
            customer_list.append(small_customer)
    except:
        customer_list=[]
    customer=forms.ChoiceField(label="customer",choices=customer_list,widget=forms.Select(attrs={"class":"form-control"}))
    session_start_date = forms.DateField(label="Session Start Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    
    amount_choice=(
        ("2500","2500"),
        ("6000","6000"),
        ("10000","10000")
    )
    amount=forms.ChoiceField(label="amount",choices=amount_choice,widget=forms.Select(attrs={"class":"form-control"}))

    session_end_date = forms.DateField(label="Session End Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))

    
class AddEventForm(forms.Form):
    eventname=forms.CharField(label="Event Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    eventdesc=forms.CharField(label="Event Description",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    eventdate = forms.DateField(label="Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    amount=forms.FloatField(label="Amount",widget=forms.NumberInput(attrs={"class":"form-control"}), min_value=0.0)


class EditEventForm(forms.Form):
    eventname=forms.CharField(label="Event Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    eventdesc=forms.CharField(label="Event Description",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    eventdate = forms.DateField(label="Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    amount=forms.FloatField(label="Amount",widget=forms.NumberInput(attrs={"class":"form-control"}), min_value=0.0)

class AddParticipationForm(forms.Form):
    participator = forms.MultipleChoiceField(
        label="Participators",
        choices=[], 
        widget=CheckboxSelectMultiple(attrs={})
    )
    EventParticipation=EventParticipation.objects.all()

    def __init__(self, *args, **kwargs):
        super(AddParticipationForm, self).__init__(*args, **kwargs)

        participator_list = []
        try:
            trainers = Trainer.objects.all()
            customers = Customer.objects.all()

            for trainer in trainers:
                small_trainer = (
                    f"trainer_{trainer.admin.first_name}_{trainer.admin.last_name}", 
                    f"{trainer.admin.first_name} {trainer.admin.last_name} (Trainer)" 
                )
                participator_list.append(small_trainer)

            for customer in customers:
                small_customer = (
                    f"customer_{customer.admin.first_name}_{customer.admin.last_name}", 
                    f"{customer.admin.first_name} {customer.admin.last_name}"  
                )
                participator_list.append(small_customer)
        except Trainer.DoesNotExist:
            participator_list = []

        self.fields['participator'].choices = participator_list

class AddCustomerLeaveForm(forms.Form):
    start_date = forms.DateField(label="To", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    end_date = forms.DateField(label="From", widget=forms.DateInput(attrs={"class": "form-control", "type": "date" }))
    description=forms.CharField(label="Description",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


class AddPaymentForm(forms.Form):
    trainer = forms.ChoiceField(label="trainer", choices=[], widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(AddPaymentForm, self).__init__(*args, **kwargs)

        trainer_list = []
        try:
            trainers = Trainer.objects.all()
            for trainer in trainers:
                small_trainer = (trainer.id, f"{trainer.admin.first_name} {trainer.admin.last_name} = {trainer.price}")
                trainer_list.append(small_trainer)
        except Trainer.DoesNotExist:
            trainer_list = []

        self.fields['trainer'].choices = trainer_list

class EditCustomerServiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditCustomerServiceForm, self).__init__(*args, **kwargs)
        customer_list=[]
        try:
            customer=Customer.objects.all()
            for customer in customer:
                small_customer=(customer.id,str(customer.admin.first_name) +"  "+str(customer.admin.last_name)) 
                customer_list.append(small_customer)
        except:
            customer_list=[]
        self.fields['customer'].choices = customer_list
    customer = forms.ChoiceField(label="customer", choices=[], widget=forms.Select(attrs={"class":"form-control"}))
    no_of_service=forms.IntegerField(label="No of Service",widget=forms.NumberInput(attrs={"class":"form-control","placeholder": "Eg: 123456"}), min_value=0, max_value=4)