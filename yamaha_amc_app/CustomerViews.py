from django.shortcuts import render
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

import uuid
import hashlib
import hmac
import base64

from yamaha_amc_app.models import CustomerDue, Customer, Event, Messages,  CustomerLeave, Trainer
from yamaha_amc_app.forms import AddCustomerLeaveForm, AddPaymentForm

def customer_home(request):
    customer = Customer.objects.filter(admin__username=request.user.username)
    customerdue = CustomerDue.objects.filter(customer_id__admin__username=request.user.username)
    current_date = date.today()
    event = Event.objects.all()
    message = Messages.objects.filter(end_date__gte=current_date)

    def genSha256(key, message):
        key = key.encode("utf-8")
        message = message.encode("utf-8")
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        return base64.b64encode(hmac_sha256.digest()).decode("utf-8")

    
    amount = 10
    tax_amount = 0
    total_amount = amount + tax_amount

    uuiid = uuid.uuid4()
    secret_key = "8gBm/:&EnhH.1/q"
    data_to_sign = f"total_amount={total_amount},transaction_uuid={uuiid},product_code=EPAYTEST"

    result = genSha256(secret_key, data_to_sign)
    print("Data to Sign:", data_to_sign)
    print("Generated Signature:", result)


    # Check if the message has already been shown in this session
    show_message = request.session.get("show_message", True)  # Default to True if not set

    # Set the session variable to False so it won't show again
    request.session["show_message"] = False

    context = {
        "due": customerdue,
        "customer": customer,
        "event": event,
        "message": message if show_message else None,  # Pass the messages only if `show_message` is True
        "current_date": current_date,
        "amount": amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "uuid": uuiid,
        "signature": result,
    }

    return render(request, "student_template/student_home_template.html", context)


def customer_detail(request):
    customer=Customer.objects.filter(admin__username=request.user.username)
    return render(request, "student_template/student_detail_template.html", {"customer": customer})

def customer_leave(request):
    form = AddCustomerLeaveForm()
    customer = Customer.objects.filter(admin__username=request.user.username)
    customerdue = CustomerDue.objects.filter(customer_id__admin__username=request.user.username)
    

    return render(request, "student_template/payment_template.html", {"form": form, "customer": customer, "due": customerdue,})

    
def save_add_customerleave(request):
    if request.method == 'POST':
        form = AddCustomerLeaveForm(request.POST)
        if form.is_valid():
            start_date= form.cleaned_data["start_date"]
            end_date= form.cleaned_data["end_date"]
            description= form.cleaned_data["description"]
            trainer=request.POST.get('trainer')
            try:
                trainer_id=Trainer.objects.get(admin__username=trainer)
                customer_id=Customer.objects.get(admin__username=request.user.username)

                CustomerLeave.objects.create(customer_id=customer_id, trainer_id=trainer_id, start_date=start_date, end_date=end_date, description=description)
                messages.success(request, "Successfully submitted leave request")
                return HttpResponseRedirect("/customer_leave_appointment")
            
            except:
                messages.error(request, "Failed to Submit Leave Request")
                return HttpResponseRedirect("/customer_leave_appointment")
        else:
            messages.error(request,"Invalid form data")
            return HttpResponseRedirect("/customer_leave_appointment")




