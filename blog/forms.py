from django import forms
from .models import Post, Instrument, Checklist, Profile
from django.contrib.auth.models import User


# form for the post model
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class InstrumentForm(forms.ModelForm):

    class Meta:
        model = Instrument
        fields = ('instrument_type','ip_address', 'ip_address_2','instrument_detector_1', 'instrument_detector_2',
                  'instrument_detector_3', 'instrument_sampler_1', 'instrument_sampler_2', 'instrument_pump',
                  'instrument_column_compartment')

class InstrumentConnectionForm(forms.ModelForm):

    class Meta:
        model = Instrument
        fields = ('instrument_connection',)


class CheckListForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = ()


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = ()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password', 'password2')
        widgets = {
            'password': forms.PasswordInput(), 'password2': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # If passwords don't match, raise a flag
        if password != password2:
            msg = forms.ValidationError("The two password fields didn't match.")
            self.add_error('password', msg)

        return self.cleaned_data


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'mobile_number', 'mobile_carrier','receive_sms_notifications', 'receive_email_notifications')

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        mobile_number = cleaned_data.get("mobile_number")
        mobile_carrier = cleaned_data.get("mobile_carrier")
        receive_sms_notifications = cleaned_data.get("receive_sms_notifications")
        email = cleaned_data.get("email")
        receive_email_notifications = cleaned_data.get("receive_email_notifications")

        # If a mobile number is typed without a carrier, raise a flag
        if mobile_number and mobile_carrier =="":
            msg = forms.ValidationError("A mobile carrier is required if you enter a mobile number")
            self.add_error('mobile_carrier', msg)

        # If a mobile carrier is typed without a number, raise a flag
        if mobile_carrier and mobile_number =="":
            msg = forms.ValidationError("A mobile number is required if you enter a mobile carrier")
            self.add_error('mobile_number', msg)

        # If sms is selected without a mobile number listed, raise a flag
        if receive_sms_notifications and mobile_number =="":
            msg = forms.ValidationError("A mobile number is required if you want sms notifications")
            self.add_error('mobile_number', msg)

        # If a mobile carrier is typed without a carrier, raise a flag
        if receive_sms_notifications and mobile_carrier == "":
            msg = forms.ValidationError("A mobile carrier is required if you want sms notifications")
            self.add_error('mobile_carrier', msg)

        # If email notifications is selected without an email raise a flag
        if receive_email_notifications and email == "":
            msg = forms.ValidationError("An email is required if you want email notifications")
            self.add_error('email', msg)


        return self.cleaned_data

class MassMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class UserMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
