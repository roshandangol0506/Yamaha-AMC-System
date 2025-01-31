from django.shortcuts import render
from datetime import date

from yamaha_amc_app.models import CustomerDue, Messages, Trainer, CustomerLeave

def trainer_detail(request):
    trainer=Trainer.objects.get(admin__username=request.user.username)

    return render(request, "staff_template/trainer_detail_template.html", {"trainer": trainer})

def trainer_home(request):
    trainer=Trainer.objects.get(admin__username=request.user.username)
    customerdue = CustomerDue.objects.filter(trainer_id=trainer) 
    current_date = date.today()
    message = Messages.objects.filter(end_date__gte=current_date)
    current_date = date.today()
    user_first_name = request.user.first_name 

    # Check if the message has already been shown in this session
    show_message = request.session.get("show_message", True)  # Default to True if not set

    # Set the session variable to False so it won't show again
    request.session["show_message"] = False

    count = 0
    for cd in customerdue:
        if cd.trainer_id.admin.first_name == user_first_name:
            count+=1
    context = {
        "user": request.user,
        "trainer": trainer,
        "customerdue": customerdue,
        "message": message if show_message else None,
        "current_date": current_date,
        "matching_count": count  
    }
    return render(request, "staff_template/staff_home_template.html", {"context": context})

def customer_leave(request):
    customerleave=CustomerLeave.objects.filter(trainer_id__admin__username=request.user.username)
    current_date = date.today()
    return render(request, "staff_template/staff_customerleave_template.html", {'customerleave': customerleave, "current_date": current_date})