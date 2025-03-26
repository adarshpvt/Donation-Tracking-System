from django.contrib import admin
from .models import Donation,BeneficiaryRequest

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'status', 'date')
    list_filter = ('status',)
    actions = ['mark_as_success']

    def mark_as_success(self, request, queryset):
        queryset.update(status='Success')
    
    mark_as_success.short_description = "Mark selected donations as Success"

admin.site.register(Donation, DonationAdmin)
from django.contrib import admin
from .models import BeneficiaryRequest

class BeneficiaryRequestAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'service_type', 'status', 'request_date')  # Fields to show in list view
    list_filter = ('status', 'service_type')  # Filters in admin panel
    actions = ['mark_as_approved', 'mark_as_rejected']  # Admin bulk actions

    def mark_as_approved(self, request, queryset):
        queryset.update(status='Approved')

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='Rejected')

    mark_as_approved.short_description = "Mark selected requests as Approved"
    mark_as_rejected.short_description = "Mark selected requests as Rejected"

admin.site.register(BeneficiaryRequest, BeneficiaryRequestAdmin)
