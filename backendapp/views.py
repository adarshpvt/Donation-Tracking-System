from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from backendapp.models import Beneficiary,BloodDonor,Product,JobApplication, JobListing
from frontendapp.models import payment_donation,ServiceRequest,blood_module
from django.utils.timezone import now
from django.db.models import Count

def admin_login(req):
    don = payment_donation.objects.all()
    total_donations=0
    for i in don:
        total_donations = total_donations + i.amount
    total_requests = ServiceRequest.objects.count()

    # Counting requests by category
    beneficiary_requests = ServiceRequest.objects.values('category').annotate(count=Count('category'))

    # Convert queryset to dictionary
    request_data = {item['category']: item['count'] for item in beneficiary_requests}
    total_donors = blood_module.objects.count()

    # Counting donors by blood group
    blood_group_counts = blood_module.objects.values('blood_group').annotate(count=Count('blood_group'))
    blood_group_data = {item['blood_group']: item['count'] for item in blood_group_counts}

    return render(req,"index.html",{'total_donations':total_donations,'total_requests':total_requests,'request_data':request_data, 'total_donors': total_donors,
        'blood_group_data': blood_group_data})

def add_donors(req):
    return render(req,"add_donors.html")

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages


import uuid
from django.shortcuts import render, redirect
from django.contrib import messages

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages

def save_donor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        category = request.POST.get('dtype')
        amount = request.POST.get('amount')
        transaction_id = request.POST.get('transaction_id')  # Get from the form

        # Ensure required fields are filled
        if not username or not category or not amount:
            messages.error(request, "Please fill in all required fields!")
            return redirect('add_donors')  # Redirect back to the form page

        # Convert amount to integer (if provided)
        amount = int(amount) if amount else None

        # If no transaction ID was generated, create one
        if not transaction_id:
            short_category = "".join([word[:2] for word in category.split()]).upper()
            unique_id = uuid.uuid4().hex[:4].upper()
            transaction_id = f"GT-{short_category}-{unique_id}"

        # Save to database
        donor = payment_donation(
            username=username,
            category=category,
            amount=amount,
            transaction_id=transaction_id
        )
        donor.save()

        messages.success(request, "Donor details saved successfully!")
        return redirect(view_donors)  # Redirect after successful submission

    return render(request, 'add_donors.html')  # Render form page if GET request





def view_donors(req):
    don=payment_donation.objects.all()
    return render(req,"view_donors.html",{'don':don})
def edit_donor(request, id):
    donor = get_object_or_404(payment_donation, id=id)
    return render(request, 'edit_donor.html', {'donor': donor})
def delete_donor(request, id):
    donor = get_object_or_404(payment_donation, id=id)
    donor.delete()
    messages.success(request, "Donor deleted successfully!")
    return redirect('view_donors')
def update_donor(request, id):
    donor = get_object_or_404(payment_donation, id=id)

    if request.method == "POST":
        donor.username = request.POST.get('username')  # Correct field name
        donor.category = request.POST.get('category')  # Correct field name
        donor.amount = request.POST.get('amount', 0)

        # Ensure transaction_id and payment_date are not altered
        donor.save()

        messages.success(request, "Donor details updated successfully!")
        return redirect('view_donors')  # Adjust this URL if necessary

    return redirect('view_donors')

from datetime import datetime
from django.utils.timezone import now
def add_beneficiary(req):
    today = datetime.today()

    ctime = today.strftime("%d/%m/%Y")
    return render(req,"add_beneficiary.html",{'ctime': ctime})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now


def save_beneficiary(request):
    if request.method == "POST":
        username = request.POST.get("username")
        category = request.POST.get("category")
        request_date = now()  # Automatically set the current date
        status = "Pending"  # Default status

        ServiceRequest.objects.create(
            username=username,
            category=category,
            request_date=request_date,
            status=status
        )

        messages.success(request, "Service request submitted successfully!")
        return redirect("view_beneficiaries")  # Update with the correct URL name
    else:
        return render(request, "add_beneficiary.html")

def view_beneficiaries(request):
    beneficiaries = ServiceRequest.objects.all()
    return render(request, 'view_beneficiaries.html', {'beneficiaries': beneficiaries})

def delete_beneficiary(request, id):
    try:
        beneficiary = ServiceRequest.objects.get(id=id)
        beneficiary.delete()
        messages.success(request, "Beneficiary deleted successfully!")
    except Beneficiary.DoesNotExist:
        messages.error(request, "Beneficiary not found!")

    return redirect('view_beneficiaries')
def edit_beneficiary(request, id):
    beneficiary = get_object_or_404(ServiceRequest, id=id)
    return render(request, 'edit_beneficiary.html', {'beneficiary': beneficiary})

def update_beneficiary(request, id):
    if request.method == "POST":
        beneficiary = get_object_or_404(ServiceRequest, id=id)
        beneficiary.username = request.POST['username']
        beneficiary.category = request.POST['category']
        beneficiary.status=request.POST['status']

        beneficiary.save()

        messages.success(request, "Beneficiary details updated successfully!")
        return redirect('view_beneficiaries')
    else:
        return redirect('view_beneficiaries')

def save_blood_donor(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        blood_group = request.POST['blood_group']
        mobile = request.POST['mobile']
        location = request.POST['location']
        availability = request.POST['availability']

        # Save to database
        blood_module.objects.create(
            full_name=full_name,
            blood_group=blood_group,
            mobile=mobile,
            location=location,
            availability=availability
        )

        messages.success(request, 'Registration Successful!')
        messages.success(request, 'Registration Successful!')
        return redirect(view_blood_donors)  # Redirect to the form page

    return render(request, 'register_blood_donor.html')
def view_blood_donors(request):
    blood_donors = blood_module.objects.all()
    return render(request, 'view_blood_donors.html', {'blood_donors': blood_donors})

def delete_blood_donor(request, id):
    try:
        blood_donor = blood_module.objects.get(id=id)
        blood_donor.delete()
        messages.success(request, "Blood donor deleted successfully!")
    except BloodDonor.DoesNotExist:
        messages.error(request, "Blood donor not found!")

    return redirect('view_blood_donors')

def edit_blood_donor(request, id):
    blood_donor = get_object_or_404(blood_module, id=id)
    return render(request, 'edit_blood_donor.html', {'blood_donor': blood_donor})

def update_blood_donor(request, id):
    if request.method == "POST":
        blood_donor = get_object_or_404(blood_module, id=id)
        blood_donor.full_name = request.POST['full_name']
        blood_donor.blood_group = request.POST['blood_group']
        blood_donor.mobile = request.POST['mobile']
        blood_donor.location = request.POST['location']
        blood_donor.availability = request.POST['availability']
        blood_donor.save()

        messages.success(request, "Blood donor details updated successfully!")
        return redirect('view_blood_donors')
    else:
        return redirect('view_blood_donors')
def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})

def save_product(request):
    if request.method == "POST":
        name = request.POST['pname']
        price = request.POST['pprice']
        quantity = request.POST['pquantity']
        image = request.FILES.get('pimage')

        product = Product(name=name, price=price, quantity=quantity, image=image)
        product.save()

        messages.success(request, "Product added successfully!")
        return redirect('view_products')
    return render(request, 'add_product.html')

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('view_products')
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'edit_product.html', {'product': product})
def update_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        product.name = request.POST['pname']
        product.price = request.POST['pprice']
        product.quantity = request.POST['pquantity']

        # Update image only if a new one is uploaded
        if 'pimage' in request.FILES:
            product.image = request.FILES['pimage']

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('view_products')
    else:
        return redirect('view_products')
def apply_job(request):
    return render(request, 'apply_job.html')

def save_job_application(request):
    if request.method == "POST":
        name = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        position = request.POST['position']
        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, "Please upload a resume.")
            return redirect('apply_job')

        job_app = JobApplication(name=name, email=email, phone=phone, position=position, resume=resume)
        job_app.save()

        messages.success(request, "Your application has been submitted successfully!")
        return redirect('apply_job')

    return render(request, 'apply_job.html')

def view_jobs(request):
    jobs = JobListing.objects.all()
    return render(request, 'view_jobs.html', {'jobs': jobs})




def requestapprove(req):
    beneficiaries=ServiceRequest.objects.all()

    return render(req,"requestapprove.html",{'beneficiaries':beneficiaries})


from django.http import JsonResponse
from frontendapp.models import ServiceRequest


def update_status(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        new_status = request.POST.get("status")

        try:
            service_request = ServiceRequest.objects.get(id=request_id)
            service_request.status = new_status
            service_request.save()
            return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        except ServiceRequest.DoesNotExist:
            return JsonResponse({"success": False, "error": "Request not found"})

    return JsonResponse({"success": False, "error": "Invalid request"})
from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render
from datetime import datetime

def my_view(request):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")  # Formatting the date
    return render(request, 'index.html', {'current_time': current_time})

def login_page(req):
    return render(req,"login.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from frontendapp.models import CustomUser  # Import CustomUser

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from frontendapp.models import CustomUser  # Ensure CustomUser is imported


def login_view(request):
    if request.method == "POST":
        un = request.POST.get('user')
        pa = request.POST.get('pass')

        # Check if username exists
        if CustomUser.objects.filter(username=un).exists():
            user = authenticate(request, username=un, password=pa)

            if user is not None:
                login(request, user)  # Securely login the user
                messages.success(request, "Login Successfully..!")

                # Redirect based on user role (adjust if necessary)
                if user.is_superuser:
                    return redirect(admin_login)
                else:
                    return redirect(admin_login)  # Change to your user dashboard view
            else:
                messages.warning(request, "Invalid password. Please try again.")
        else:
            messages.warning(request, "Invalid username. Please check and try again.")

    return redirect(login_page)  # Redirect back to login page if login fails

