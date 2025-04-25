from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from decimal import Decimal
import pdfkit,io
from reportlab.pdfgen import canvas
from .models import CustomUser, Donation,signupdb,payment_donation,BloodModule,Organ_Donor,Organ
from django.utils.timezone import now


# Public Views
def main_page(request):
    volunteers = Volunteer.objects.filter(is_approved=1)  # Only show approved volunteers

    return render(request, "main.html",{'volunteers':volunteers})

def about(request):
    return render(request, "about.html")

def volunteer(request):
    return render(request, "volunteer.html")

def blog(request):
    return render(request, "blog.html")

def events(request):
    return render(request, "events.html")

def contact(request):
    return render(request, "contact.html")

import razorpay
from django.shortcuts import render
from .models import payment_donation  # Ensure correct model import

def bedonar(request):
    name = payment_donation.objects.all()
    customer = payment_donation.objects.order_by('-id').first()  # Get the latest entry

    user_details = {
        'username': request.session.get('username'),
        'email': request.session.get('email')
    }

    if customer:
        pays = customer.amount
        amount = int(pays * 100)  # Convert to paisa
        pay_str = str(amount)
    else:
        pays = 0  # Set a default value if no record exists
        amount = 0
        pay_str = "0"

    # Debugging
    print(f"Latest donation: {pays}, Amount in paisa: {amount}")

    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_QzIn7XrT0zJ9If', '9jM71BiWU9CXbvXJd0IZSuTl'))
        payment = client.order.create({'amount': amount, 'currency': order_currency})

    return render(request, "bedonar.html", {'customer': customer, 'pay_str': pay_str, 'user_details': user_details})







def login_form(request):
    return render(request, "login_form.html")

# User Authentication

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
 # Ensure this is the correct import for your model


def save_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')


        if password != cpassword:
            messages.error(request, "Passwords do not match!")
            return redirect(login_form)

        if signupdb.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect(login_form)

        hashed_password = make_password(password)  # Securely store password
        user = signupdb(username=username, email=email, password=hashed_password,cpassword=cpassword)
        user.save()
        messages.success(request, "Sign-up successful! Please log in.")

    return render(request, 'login_form.html')

def save_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = signupdb.objects.get(username=username)

            # Check password
            if check_password(password, user.password):  # Compare hashed password
                request.session['user_id'] = user.id  # Store user session
                request.session['username'] = user.username
                messages.success(request, f"Welcome, {user.username},to the GiveTrack !")
                return redirect(main_page)  # Redirect to dashboard
            else:
                messages.error(request, "Invalid password!")

        except signupdb.DoesNotExist:
            messages.error(request, "User does not exist!")

        return redirect(login_form)

    return render(request, 'login_form.html')





def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out successfully.")
    return redirect('login_form')

# User Dashboards




def beneficiary_dashboard(request):
    return render(request, 'beneficiary_dashboard.html')







def donation(req):
    return render(req,"donation.html")





def mydonations(req):
    if 'username' not in req.session:  # Check if user session exists
        return redirect(login_form)  # Redirect to login page if not logged in

    username = req.session['username']  # Get username from session
    payment_details = payment_donation.objects.filter(username=username)
    subtotal=0
    for i in payment_details:
        subtotal = subtotal + i.amount
    context = {
        'username': username,
        'payment_details': payment_details,

        'subtotal': subtotal
    }
    return render(req,"mydonation.html",context)


import razorpay
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import payment_donation
import uuid

# Razorpay credentials
razorpay_client = razorpay.Client(auth=("rzp_test_QzIn7XrT0zJ9If", "9jM71BiWU9CXbvXJd0IZSuTl"))


@csrf_exempt
def save_pay_donation(request):
    if request.method == "POST":
        username = request.POST.get("username")
        category = request.POST.get("category")
        transaction_id = request.POST.get("transaction_id")  # ✅ Get transaction_id from frontend

        # ✅ Handle amount parsing safely
        try:
            amount = int(request.POST.get("amt"))
            if amount <= 0:
                return JsonResponse({"success": False, "message": "Invalid amount"})
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "message": "Invalid amount format"})

        # ✅ Save donation data to DB with the front-end generated transaction_id
        donation = payment_donation.objects.create(
            username=username,
            category=category,
            amount=amount,
            transaction_id=transaction_id,  # ✅ Use the correct transaction ID
        )

        # ✅ Create Razorpay order with the saved amount
        order_data = {
            "amount": amount * 100,  # Convert to paise
            "currency": "INR",
            "payment_capture": "1"
        }
        order = razorpay_client.order.create(order_data)

        # ✅ Store Razorpay order ID if needed
        donation.razorpay_order_id = order["id"]
        donation.save()

        # ✅ Return JSON response with order details
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt
def process_payment(request):
    order_id = request.GET.get("order_id")
    amount = request.GET.get("amount")
    username = request.GET.get("username")
    category = request.GET.get("category")

    # Render a payment page with Razorpay options
    return render(
        request,
        "process_payment.html",
        {
            "order_id": order_id,
            "amount": amount,
            "username": username,
            "category": category,
            "razorpay_key": "rzp_test_QzIn7XrT0zJ9If",
        },
    )
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        try:
            # Verify Razorpay signature
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                # ✅ Update payment_donation with payment details
                donation = payment_donation.objects.get(transaction_id=order_id)
                donation.transaction_id = payment_id
                donation.payment_status = "Success"
                donation.save()

                return redirect("/thank-you/")  # Redirect to thank you page

        except Exception as e:
            print(f"❌ Razorpay Verification Failed: {str(e)}")
            return redirect("/payment-failed/")

    return JsonResponse({"success": False, "message": "Invalid request"})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import payment_donation


def payment_success(request):
    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        payment_id = request.POST.get("payment_id")
        payment_status = request.POST.get("payment_status")

        # Update payment status
        try:
            donation = payment_donation.objects.get(transaction_id=transaction_id)
            donation.payment_id = payment_id
            donation.payment_status = payment_status
            donation.save()

            return render(request, "thank_you.html", {"transaction_id": transaction_id})

        except payment_donation.DoesNotExist:
            return HttpResponse("Invalid Transaction ID")

    return redirect("main_page")












from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from .models import payment_donation

def generate_single_payment_pdf(request, transaction_id):
    # Fetch the specific payment record
    payment = get_object_or_404(payment_donation, transaction_id=transaction_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_{transaction_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, height - 50, "Donation Payment Receipt")

    # Payment Details
    p.setFont("Helvetica-Bold", 12)
    y = height - 100
    p.drawString(50, y, "Transaction ID:")
    p.drawString(200, y, payment.transaction_id)

    y -= 30
    p.drawString(50, y, "Donor Username:")
    p.drawString(200, y, payment.username)

    y -= 30
    p.drawString(50, y, "Category:")
    p.drawString(200, y, payment.category)

    y -= 30
    p.drawString(50, y, "Amount (Rs.):")
    p.drawString(200, y, str(payment.amount))

    y -= 30
    p.drawString(50, y, "Payment Date:")
    p.drawString(200, y, payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'))

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 50, "Thank you for your donation!")

    p.showPage()
    p.save()
    return response

def beneficiary(req):
    user_details = {
        'username': req.session.get('username'),
        'email': req.session.get('email')
    }

    return render(req,"beneficiary.html",{'user_details':user_details})
def trackbeneficiary(req):
    track=ServiceRequest.objects.all()
    username = req.session['username']  # Get username from session
    track_details = ServiceRequest.objects.filter(username=username)
    return render(req,"trackbenefic.html",{'track':track,'track_details':track_details})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import ServiceRequest


def request_service(request):
    if request.method == "POST":
        username = request.POST.get("username")
        category = request.POST.get("category")

        # Check if the request already exists
        existing_request = ServiceRequest.objects.filter(username=username, category=category).exists()

        if existing_request:
            messages.error(request, "You have already requested this service.")
            return redirect("beneficiary")  # Redirect back to the same page

        # If no existing request, create a new one
        ServiceRequest.objects.create(
            username=username,
            category=category,
            status="Pending"
        )

        messages.success(request, "Your request has been submitted successfully!")
        return redirect("beneficiary")  # Redirect to the same page or a success page

    return redirect("beneficiary")

def blood(req):
    return render(req,"blood.html")


def blood_re(req):
    return render(req,"blood_re.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BloodModule

def save_blooddonor(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        blood_group = request.POST.get('blood_group')
        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        state = request.POST.get('state')
        city = request.POST.get('city')
        recent_donation = request.POST.get('recent_donation')
        chronic_diseases = request.POST.get('chronic_diseases')
        recent_procedure = request.POST.get('recent_procedure')
        pregnant_or_breastfeeding = request.POST.get('pregnant_or_breastfeeding')
        recent_vaccination = request.POST.get('recent_vaccination')

        # Ensure all required fields are provided
        if not all([full_name, blood_group, mobile, age, state, city]):
            messages.error(request, "All fields are required.")
            return redirect(blood_re)  # Redirect to the form page

        # Save donor details
        donor = BloodModule(
            full_name=full_name,
            blood_group=blood_group,
            mobile=mobile,
            age=age,
            state=state,
            city=city,
            recent_donation=recent_donation == 'Yes',  # Convert to Boolean
            chronic_diseases=chronic_diseases == 'Yes',
            recent_procedure=recent_procedure == 'Yes',
            pregnant_or_breastfeeding=pregnant_or_breastfeeding == 'Yes',
            recent_vaccination=recent_vaccination == 'Yes',
        )
        donor.save()

        messages.success(request, "Blood donor registered successfully!")
        return redirect(blood)  # Redirect to donor list page (adjust as needed)

    return render(request, 'blood_re.html')






from django.shortcuts import render
from django.http import JsonResponse
import json

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BloodModule  # Ensure correct import

@csrf_exempt  # Use CSRF protection in production
def search_donors(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            blood_group = data.get("blood_group")
            city = data.get("city")  # Change 'location' to 'city'

            # Filter donors based on blood group and city
            donors = BloodModule.objects.filter(blood_group=blood_group, city__icontains=city)

            donor_list = list(donors.values("full_name", "blood_group", "city", "mobile","age","state"))  # Use city instead of location

            return JsonResponse(donor_list, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("Error:", str(e))  # Debugging output
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.http import HttpResponseForbidden

def csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please reload the page and try again.")

import razorpay
from django.http import JsonResponse
from django.conf import settings

# Razorpay API Key and Secret
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(request):
    if request.method == "POST":
        amount = int(request.POST.get('amt')) * 100  # Convert to paise
        currency = "INR"

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": "1",
        })

        if razorpay_order:
            return JsonResponse({
                "success": True,
                "payment_order_id": razorpay_order['id'],
                "amount": amount // 100,  # Send back the original amount
            })
        else:
            return JsonResponse({"success": False, "error": "Failed to create Razorpay order."})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})

def thank_you(request):
    last_payment = payment_donation.objects.filter(username=request.session.get("username")).order_by('-id').first()

    return render(request, "thank_you.html",{"last_payment":last_payment})

def organ(req):
    return render(req,"organ.html")


from django.shortcuts import render, redirect
from frontendapp.models import Organ_Donor, Organ

def submit_donor(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        emergency_contact = request.POST.get("emergency_contact")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        blood_group = request.POST.get("blood_group")
        weight = request.POST.get("weight")
        chronic_disease = request.POST.get("chronic_disease") == "yes"
        chronic_details = request.POST.get("chronic_details", "")
        surgery = request.POST.get("surgery") == "yes"
        surgery_details = request.POST.get("surgery_details", "")
        medications = request.POST.get("medications") == "yes"
        medications_details = request.POST.get("medications_details", "")

        # Get selected organs
        organ_values = request.POST.getlist("organs[]")
        print("Selected Organs:", organ_values)  # Debugging line



        # Create the donor entry
        donor = Organ_Donor.objects.create(
            full_name=full_name,
            dob=dob,
            email=email,
            phone=phone,
            gender=gender,
            emergency_contact=emergency_contact,
            address=address,
            city=city,
            state=state,
            country=country,
            blood_group=blood_group,
            weight=weight,
            chronic_disease=chronic_disease,
            chronic_details=chronic_details,
            surgery=surgery,
            surgery_details=surgery_details,
            medications=medications,
            medications_details=medications_details,
        )

        organ_objects = Organ.objects.filter(name__in=[o.capitalize() for o in organ_values])
        print("Organ Objects Found:", organ_objects)  # Debugging step
        donor.organs.set(organ_objects)  # ✅ Correct way to assign many-to-many

        return redirect(main_page)  # Change to your actual success URL

    return render(request, "organ.html")
from django.shortcuts import render, redirect
from frontendapp.models import Volunteer
from django.contrib import messages

def volunteer_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        profile_pic = request.FILES.get('profilePic')  # handles file input

        # Save the data to the model
        Volunteer.objects.create(
            name=name,
            email=email,
            address=address,
            city=city,
            phone=phone,
            profile_pic=profile_pic
        )
        messages.success(request, "Volunteer Registered Successfully!")
        return redirect(main_page)  # or any success page

    return render(request, 'volunteer.html')  # replace with your template
