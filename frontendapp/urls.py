from django.urls import path
from frontendapp import views


urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('about/', views.about, name="about"),
    path('volunteer/', views.volunteer, name="volunteer"),
    path('blog/', views.blog, name="blog"),
    path('events/', views.events, name="events"),
    path('contact/', views.contact, name="contact"),
    path('bedonar/', views.bedonar, name="bedonar"),
    path('login_form/', views.login_form, name="login_form"),
    path('donation/', views.donation, name="donation"),

    # Authentication Routes
    path('save_signup/', views.save_signup, name="save_signup"),
    path('save_signin/', views.save_signin, name="save_signin"),
    path('logout/', views.logout_user, name="logout"),
    path('save_pay_donation/', views.save_pay_donation, name="save_pay_donation"),
    path('mydonations/', views.mydonations, name="mydonations"),
    path('generate_single_payment_pdf/<str:transaction_id>/', views.generate_single_payment_pdf, name="generate_single_payment_pdf"),


    path('beneficiary/', views.beneficiary, name="beneficiary"),
    path('trackbeneficiary/', views.trackbeneficiary, name="trackbeneficiary"),
    path('request_service/', views.request_service, name="request_service"),
    path('blood/', views.blood, name="blood"),
    path('blood_re/', views.blood_re, name="blood_re"),
    path('save_blooddonor/', views.save_blooddonor, name="save_blooddonor"),
    path('search_donors/', views.search_donors, name="search_donors"),
    path('create_razorpay_order/', views.create_razorpay_order, name="create_razorpay_order"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('thank_you/', views.thank_you, name="thank_you"),
    path('organ/', views.organ, name="organ"),
    path('submit_donor/', views.submit_donor, name="submit_donor"),
    path('volunteer_register/', views.volunteer_register, name="volunteer_register"),
]



