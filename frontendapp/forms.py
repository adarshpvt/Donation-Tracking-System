from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'full_name', 'email', 'phone_number', 'address']
from django import forms
from .models import BloodModule

class BloodModuleForm(forms.ModelForm):
    class Meta:
        model = BloodModule
        fields = '__all__'
        exclude = ['registered_at']

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18 or age > 65:
            raise forms.ValidationError("Age must be between 18 and 65.")
        return age

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(str(mobile)) != 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        return mobile