from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from backendapp.models import Beneficiary,BloodDonor,Product,JobApplication, JobListing
from frontendapp.models import payment_donation,ServiceRequest,BloodModule,Volunteer
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
    total_donors = BloodModule.objects.count()

    # Counting donors by blood group
    blood_group_counts = BloodModule.objects.values('blood_group').annotate(count=Count('blood_group'))
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
        age = int(request.POST['age'])  # Convert age to integer
        blood_group = request.POST['blood_group']
        mobile = request.POST['mobile']
        state = request.POST['state']
        city = request.POST['city']
        recent_donation = request.POST['recent_donation']
        chronic_diseases = request.POST['chronic_diseases']
        recent_procedure = request.POST['recent_procedure']
        pregnant_or_breastfeeding = request.POST['pregnant_or_breastfeeding']
        recent_vaccination = request.POST['recent_vaccination']

        # Validate age (between 18 and 65)
        if age < 18 or age > 65:
            messages.error(request, "Age must be between 18 and 65.")
            return redirect('register_blood_donor')

        # Save to database
        BloodModule.objects.create(
            full_name=full_name,
            age=age,
            blood_group=blood_group,
            mobile=mobile,
            state=state,
            city=city,
            recent_donation=recent_donation,
            chronic_diseases=chronic_diseases,
            recent_procedure=recent_procedure,
            pregnant_or_breastfeeding=pregnant_or_breastfeeding,
            recent_vaccination=recent_vaccination
        )

        messages.success(request, 'Registration Successful!')
        return redirect('view_blood_donors')  # Redirect to the donor list page

    return render(request, 'register_blood_donor.html')

def view_blood_donors(request):
    blood_donors = BloodModule.objects.all()
    return render(request, 'view_blood_donors.html', {'blood_donors': blood_donors})

def delete_blood_donor(request, id):
    try:
        blood_donor = BloodModule.objects.get(id=id)
        blood_donor.delete()
        messages.success(request, "Blood donor deleted successfully!")
    except BloodDonor.DoesNotExist:
        messages.error(request, "Blood donor not found!")

    return redirect('view_blood_donors')

def edit_blood_donor(request, id):
    blood_donor = get_object_or_404(BloodModule, id=id)
    return render(request, 'edit_blood_donor.html', {'blood_donor': blood_donor})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from frontendapp.models import BloodModule  # Ensure this is your correct model

def update_blood_donor(request, id):
    blood_donor = get_object_or_404(BloodModule, id=id)

    if request.method == "POST":
        blood_donor.full_name = request.POST.get('full_name', blood_donor.full_name)
        blood_donor.blood_group = request.POST.get('blood_group', blood_donor.blood_group)
        blood_donor.mobile = request.POST.get('mobile', blood_donor.mobile)
        blood_donor.age = request.POST.get('age', blood_donor.age)
        blood_donor.state = request.POST.get('state', blood_donor.state)
        blood_donor.city = request.POST.get('city', blood_donor.city)

        # ✅ Fix: Ensure Yes/No fields are correctly stored
        blood_donor.recent_donation = request.POST.get('donated_last_3_months', 'No')
        blood_donor.chronic_diseases = request.POST.get('chronic_diseases', 'No')
        blood_donor.recent_procedure = request.POST.get('recent_surgery_tattoo', 'No')
        blood_donor.pregnant_or_breastfeeding = request.POST.get('pregnant_or_breastfeeding', 'No')
        blood_donor.recent_vaccination = request.POST.get('recent_vaccination', 'No')

        blood_donor.save()

        messages.success(request, "Blood donor details updated successfully!")
        return redirect('view_blood_donors')

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

        volunteers = Volunteer.objects.all()  # Fetch all registered volunteers
        return render(request, 'view_jobs.html', {'volunteers': volunteers})




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


from django.shortcuts import render, redirect
from django.contrib import messages
from frontendapp.models import Organ, Organ_Donor


def register_organ_donor(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        emergency_contact = request.POST.get("emergency_contact")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        weight = request.POST.get("weight")

        chronic_disease = request.POST.get("chronic_disease") == "True"
        chronic_details = request.POST.get("chronic_details", "")

        surgery = request.POST.get("surgery") == "True"
        surgery_details = request.POST.get("surgery_details", "")

        medications = request.POST.get("medications") == "True"
        medications_details = request.POST.get("medications_details", "")

        organ_ids = request.POST.getlist("organs")  # Get list of selected organ IDs

        # Create and save donor object
        donor = Organ_Donor.objects.create(
            full_name=full_name,
            dob=dob,
            email=email,
            phone=phone,
            emergency_contact=emergency_contact,
            address=address,
            city=city,
            state=state,
            country=country,
            gender=gender,
            blood_group=blood_group,
            weight=weight,
            chronic_disease=chronic_disease,
            chronic_details=chronic_details,
            surgery=surgery,
            surgery_details=surgery_details,
            medications=medications,
            medications_details=medications_details,
        )

        # Add selected organs to donor
        donor.organs.set(organ_ids)  # ManyToManyField requires .set()

        messages.success(request, "Organ donor registered successfully!")
        return redirect(view_organ_donors)  # Redirect to the same form page

    organs = Organ.objects.all()
    return render(request, "register_organ_donor.html", {"organs": organs})



from django.shortcuts import render, get_object_or_404, redirect
from frontendapp.models import Organ_Donor
from django.contrib import messages

def view_organ_donors(request):
    organ_donors = Organ_Donor.objects.all()
    return render(request, 'view_organ_donors.html', {'organ_donors': organ_donors})

def delete_organ_donor(request, id):
    donor = get_object_or_404(Organ_Donor, id=id)
    donor.delete()
    messages.success(request, "Organ donor record deleted successfully!")
    return redirect('view_organ_donors')


def edit_organ_donor(request, donor_id):
    donor = get_object_or_404(Organ_Donor, id=donor_id)

    if request.method == "POST":
        donor.full_name = request.POST.get("full_name")
        donor.dob = request.POST.get("dob")
        donor.email = request.POST.get("email")
        donor.phone = request.POST.get("phone")
        donor.emergency_contact = request.POST.get("emergency_contact")
        donor.address = request.POST.get("address")
        donor.city = request.POST.get("city")
        donor.state = request.POST.get("state")
        donor.country = request.POST.get("country")
        donor.gender = request.POST.get("gender")
        donor.blood_group = request.POST.get("blood_group")
        donor.weight = request.POST.get("weight")

        donor.chronic_disease = request.POST.get("chronic_disease") == "True"
        donor.chronic_details = request.POST.get("chronic_details", "")

        donor.surgery = request.POST.get("surgery") == "True"
        donor.surgery_details = request.POST.get("surgery_details", "")

        donor.medications = request.POST.get("medications") == "True"
        donor.medications_details = request.POST.get("medications_details", "")

        organ_ids = request.POST.getlist("organs")
        donor.organs.set(organ_ids)

        donor.save()

        messages.success(request, "Organ donor details updated successfully!")
        return redirect(view_organ_donors)

    organs = Organ.objects.all()
    selected_organs = list(donor.organs.values_list("id", flat=True))  # ✅ Fix applied

    return render(request, "edit_organ_donor.html", {
        "donor": donor,
        "organs": organs,
        "selected_organs": selected_organs,
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from frontendapp.models import Volunteer

def save_volunteer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        profile_pic = request.FILES.get('profilePic')

        Volunteer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            profile_pic=profile_pic
        )

        messages.success(request, "Volunteer Registered Successfully!")
        return redirect(view_jobs)  # change this to your success page

    return render(request, 'apply_job.html')  # make sure this matches your template name

def volunteer_approval(req):
    volunteers = Volunteer.objects.all()
    return render(req,"volunteer_approval.html",{'volunteers':volunteers})
def edit_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)  # Fetch volunteer by name

    if request.method == "POST":
        volunteer.name = request.POST['name']
        volunteer.email = request.POST['email']
        volunteer.phone = request.POST['phone']
        volunteer.city = request.POST['city']

        if 'profile_pic' in request.FILES:  # Update profile picture if uploaded
            volunteer.profile_pic = request.FILES['profile_pic']

        volunteer.save()
        messages.success(request, "Volunteer details updated successfully!")
        return redirect('view_jobs')  # Redirect to the volunteer list page

    return render(request, 'edit_volunteer.html', {'volunteer': volunteer})
def delete_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    volunteer.delete()
    messages.success(request, "Volunteer deleted successfully!")
    return redirect('view_jobs')
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from frontendapp.models import Volunteer

def approve_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    volunteer.is_approved = True
    volunteer.save()
    messages.success(request, f"{volunteer.name} has been approved.")
    return redirect(volunteer_approval)  # Change to your admin view name

def decline_volunteer(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    volunteer.is_approved = False
    volunteer.save()
    messages.warning(request, f"{volunteer.name} has been declined.")
    return redirect(volunteer_approval)  # Change to your admin view name
