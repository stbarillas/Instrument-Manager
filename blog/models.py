from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import *


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Instrument(models.Model):
    # tuple of instrument labels
    instrument_options = (
        ('LC', 'LC'),
        ('LCMS', 'LCMS'),
        ('GC', 'GC'),
        ('GCMS', 'GCMS'),
    )
    # tuple of instrument status options
    instrument_status_options = (
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Out of Order', 'Out of Order'),
    )

    instrument_type = models.CharField(max_length=50, choices=instrument_options, default='LC')
    instrument_status = models.CharField(max_length=50, choices=instrument_status_options, default='Available')
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    ip_address_2 = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    # added instrument name to create unique identifier for the waitlist entries
    instrument_name = models.CharField(max_length=50)
    instrument_image = models.ImageField(upload_to='images')
    instrument_current_owner = models.ForeignKey(User, unique=False, null=True, blank= True)
    instrument_connection = models.BooleanField(default=True)
    instrument_detector_1 = models.CharField(max_length=50, null=True, blank=True)
    instrument_detector_2 = models.CharField(max_length=50, null=True, blank=True)
    instrument_detector_3 = models.CharField(max_length=50, null=True, blank=True)
    instrument_sampler_1 = models.CharField(max_length=50, null=True, blank=True)
    instrument_sampler_2 = models.CharField(max_length=50, null=True, blank=True)
    instrument_pump = models.CharField(max_length=50, null=True, blank=True)
    instrument_column_compartment = models.CharField(max_length=50, null=True, blank=True)


    def publish(self):
        return self.save

    # This returns the instrument type as a string. Shows instrument type as name in admin console
    def __str__(self):
        return self.instrument_type + " " + self.ip_address

    class Meta:
        # This ensures instrument type and ip address combination is unique for model form validation
        unique_together = ('instrument_type', 'ip_address')


class Checklist(models.Model):
    user = models.ForeignKey(User, unique=False)
    display_name = models.CharField(max_length=50)
    instrument_pk = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    ownership_date = models.DateTimeField(default=timezone.now())

    def publish(self):
        return self.save

    def __str__(self):
        return str(self.instrument_pk)

# Note: User and Profile models are linked One-to-One
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField()
    receive_email_notifications = models.BooleanField(default=False)
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        help_text='Optional'
    )
    # tuple with carrier domains. These get added to phone numbers in order to text users
    carrier_options = (
        (None, ''),
        ('@txt.att.net', 'AT&T'),
        ('@messaging.sprintpcs.com', 'Sprint'),
        ('@tmomail.net', 'T-Mobile'),
        ('@vtext.com', 'Verizon'),
    )
    mobile_carrier = models.CharField(max_length=25, choices=carrier_options, blank=True,
                                      help_text='Optional')

    receive_sms_notifications = models.BooleanField(default=False)


    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def is_manager(self):
        # self wasn't a user instance so a query to pull the instance was needed
        user = User.objects.get(username = self)
        if Profile.objects.filter(manager = user):
            return True
        else:
            return False

    def publish(self):
        return self.save

    def __str__(self):
        return str(self.user)





