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
from .models import CustomUser, Donation,signupdb,payment_donation,blood_module
from django.utils.timezone import now


# Public Views
def main_page(request):
    return render(request, "main.html")

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
from django.http import JsonResponse
from .models import payment_donation

def save_pay_donation(request):
    razorpay_client = razorpay.Client(auth=("rzp_test_QzIn7XrT0zJ9If", "9jM71BiWU9CXbvXJd0IZSuTl"))
    if request.method == "POST":
        username = request.POST.get("username")
        category = request.POST.get("category")
        amount = int(request.POST.get("amt")) * 100  # Convert to paise
        transaction_id = request.POST.get("transaction_id") # Convert to paise
        payment_date = request.POST.get("amt") # Convert to paise


        # 1️⃣ Save donation in the database
        donation = payment_donation.objects.create(
            username=username,
            category=category,
            amount=amount / 100,
            transaction_id=transaction_id,
            payment_date=payment_date# Convert back to INR
        )


        # 2️⃣ Create Razorpay order
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        return JsonResponse({
            "success": True,
            "payment_order_id": order["id"],
            "amount": amount
        })

    return JsonResponse({"success": False, "message": "Invalid request"})







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


def save_blooddonor(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        blood_group = request.POST.get('blood_group')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        availability = request.POST.get('availability')

        # Save donor details
        donor = blood_module(
            full_name=full_name,
            blood_group=blood_group,
            mobile=mobile,
            location=location,
            availability=availability
        )
        donor.save()

        messages.success(request, "Blood donor registered successfully!")
        return redirect(blood)  # Redirect to the blood donor list page

    return render(request, 'blood_re.html')






from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import blood_module

def search_donors(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request
            blood_group = data.get("blood_group")
            location = data.get("location")

            # Filter donors based on blood group and location
            donors = blood_module.objects.filter(blood_group=blood_group, location__icontains=location)

            donor_list = list(donors.values("full_name", "blood_group", "location", "mobile"))

            return JsonResponse(donor_list, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.http import HttpResponseForbidden

def csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please reload the page and try again.")


