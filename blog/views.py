import os
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Instrument, Checklist, Profile
from .forms import PostForm, InstrumentForm, CheckListForm, ProfileForm, ReleaseForm, UserForm, MassMessageForm, \
    InstrumentConnectionForm, UserMessageForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage, send_mass_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.views.static import serve
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .tasks import massMessageSend


@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def instrument_list(request):
        # pulls all instruments from instrument model
    instruments = Instrument.objects.all().order_by('instrument_name')

    # pulls all checklists from checklist model
    checklists = Checklist.objects.all().order_by('created_date')
    # takes instruments, pushes them to template with variable 'instruments'
    return render(request, 'blog/instrument_list.html', {'instruments': instruments, 'checklists': checklists})

def instrument_status(pk):
    instrument = Instrument.objects.get(pk=pk)
    if instrument.instrument_status == 'Out of Order':
        pass
    elif Checklist.objects.filter(instrument_pk=pk):
        instrument.instrument_status = 'In Use'
        instrument.save()
    else:
        instrument.instrument_status = 'Available'
        instrument.save()

def instrument_owner(pk):
    instrument = Instrument.objects.get(pk=pk)

    # checks if instrument has any wait list entries
    if Checklist.objects.filter(instrument_pk=pk):
        current_owner = Checklist.objects.filter(instrument_pk=pk).order_by('created_date')[0]

        # publish an ownership time for oldest checklist object and save result
        current_owner.ownership_date = timezone.now()
        current_owner.save()

        # assign instrument owner as user from oldest wait list entry for that particular instrument
        instrument.instrument_current_owner = current_owner.user
        instrument.save()

    # if no wait list entries found, current user is set to None
    else:
        instrument.instrument_current_owner = None
        instrument.save()



@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def instrument_new(request):
    if request.method == "POST":
        form = InstrumentForm(request.POST)
        if form.is_valid():
            instrument = form.save(commit=False)
            instrument.instrument_name = instrument.instrument_type + " " + instrument.ip_address

            # assign instrument image based on instrument type
            if instrument.instrument_type =='LCMS':
                instrument.instrument_image = 'images/singlequad.jpg'
            if instrument.instrument_type =='GCMS':
                instrument.instrument_image = 'images/5977B.jpg'
            if instrument.instrument_type =='LC':
                instrument.instrument_image = 'images/1290.jpg'
            if instrument.instrument_type =='GC':
                instrument.instrument_image = 'images/7890b.jpg'
            instrument.save()
            return redirect('instrument_list')

    else:
        form = InstrumentForm()
    return render(request, 'blog/instrument_new.html', {'form': form})

@login_required
def instrument_edit(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if request.method == "POST":
        form = InstrumentForm(request.POST, instance=instrument)
        if form.is_valid():
            instrument = form.save(commit=False)
            instrument.instrument_name = instrument.instrument_type + " " + instrument.ip_address

            # assign instrument image based on instrument type
            if instrument.instrument_type == 'LCMS':
                instrument.instrument_image = 'images/singlequad.jpg'
            if instrument.instrument_type == 'GCMS':
                instrument.instrument_image = 'images/5977B.jpg'
            if instrument.instrument_type == 'LC':
                instrument.instrument_image = 'images/1290.jpg'
            if instrument.instrument_type == 'GC':
                instrument.instrument_image = 'images/7890b.jpg'
            instrument.save()
            return redirect('instrument_list')

    else:
        form = InstrumentForm(instance=instrument)
    return render(request, 'blog/instrument_edit.html', {'form': form})

@login_required
def instrument_detail(request, pk):

    instrument = get_object_or_404(Instrument, pk=pk)
    checklist = Checklist.objects.filter(instrument_pk=instrument.pk).order_by('created_date')

    return render(request, 'blog/instrument_detail.html', {'instrument': instrument, 'checklists':checklist})

@login_required
def checkout_detail(request, pk):

    instrument = get_object_or_404(Instrument, pk=pk)
    # Variable to track if user is on waitlist for this instrument
    onlist = False
    # Filters wait list for current instrument and user. if the list is not empty, you are redirected to the homepage
    if Checklist.objects.filter(instrument_pk=instrument.pk).filter(user=request.user):
        onlist = True

    if request.method == "POST":
        form = CheckListForm(request.POST)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.user = request.user
            checklist.display_name = request.user.profile.get_full_name()
            checklist.instrument_pk = pk
            checklist.save()
            # Run instrument status update function
            instrument_status(pk)
            # Run instrument owner update function
            instrument_owner(pk)

            return redirect('instrument_list')
    else:
        form = CheckListForm()
    return render(request, 'blog/checkout_detail.html', {'form': form, 'instrument':instrument, 'onlist':onlist})

@login_required
def release_detail(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    # Variable to track if user is on waitlist for this instrument
    onlist = True
    # Filters wait list for current instrument and user. if the list is not empty, you are redirected to error page
    if not Checklist.objects.filter(instrument_pk=pk).filter(user=request.user):
        onlist = False
    if request.method == "POST":
        form = ReleaseForm(request.POST)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.user = request.user
            checklist.instrument_pk = pk
            release = Checklist.objects.filter(instrument_pk=checklist.instrument_pk).filter(user=checklist.user)

            # Pull the current owner at the top of the waitlist for current instrument
            current_owner = Checklist.objects.filter(instrument_pk=checklist.instrument_pk).order_by('created_date')[0]
            release.delete()
            # Run instrument status update function
            instrument_status(pk)
            # Run instrument owner update function
            instrument_owner(pk)
            # Checks if current user is also the current instrument owner
            # This should be replaced with a function that checks if the top entry has changed instead of comparing
            # the current user. Otherwise admin intervention will not result in an email
            if request.user == current_owner.user:
                # Pull the new owner at the top of the waitlist for current instrument
                new_owner = Checklist.objects.filter(instrument_pk=checklist.instrument_pk).order_by('created_date')
                # If new_owner isn't empty, proceed with sending email
                if new_owner:
                    new_owner = Checklist.objects.filter(instrument_pk=checklist.instrument_pk).order_by('created_date')[0]
                    print(new_owner.user)
                    email_send(checklist.instrument_pk, new_owner.user)
            else:
                print('no email sent')
            return redirect('instrument_list')
    else:
        form = ReleaseForm()
    return render(request, 'blog/release_detail.html', {'form': form, 'instrument':instrument, 'onlist':onlist})

def email_send(instrument_pk, instrument_owner):
    full_name = instrument_owner.profile.get_full_name()
    user_email = instrument_owner.profile.email
    user_number = instrument_owner.profile.mobile_number
    instrument_name = Instrument.objects.get(pk=instrument_pk).instrument_name
    print(instrument_name)
    subject_line = 'Instrument ' + instrument_name + ' is ready'
    message_text = 'But are you ready ' + full_name + '?'
    mobile_carrier = instrument_owner.profile.mobile_carrier
    sms_email = user_number + mobile_carrier
    recipient_list = []
    if instrument_owner.profile.receive_email_notifications:
        recipient_list.append(user_email)
    if instrument_owner.profile.receive_sms_notifications:
        recipient_list.append(sms_email)
    if recipient_list:
        massMessageSend.delay(subject_line, message_text, recipient_list)
        massMessageSend.delay(subject_line, message_text, recipient_list)
    return

def mass_message (request):
    if request.method == "POST":
        form = MassMessageForm(request.POST,)
        if form.is_valid():
            recipient_list = []
            all_profiles = Profile.objects.all()
            subject_line = "RAM Mass Message Alert from " + str(request.user.profile.first_name) + " " + str(request.user.profile.last_name)
            message_text = form.cleaned_data['message']
            for profile in all_profiles:
                if profile.email:
                    recipient_list.append(profile.email)
                if profile.mobile_number:
                    sms_email = profile.mobile_number + profile.mobile_carrier
                    recipient_list.append(sms_email)
            if recipient_list:
                massMessageSend.delay(subject_line, message_text, recipient_list)
            return redirect('instrument_list')

    else:
        form = MassMessageForm()
    return render(request, 'blog/mass_message.html', {'form': form})

def register(request):

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Now we hash the password with the set_password method. Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            # Since we need to set the user attribute, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('instrument_list')

        # Invalid form or forms - mistakes or something else? Print problems to the terminal. They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    # Render the template depending on the context.
    return render(request,'blog/register.html',
                  {'user_form': user_form, 'profile_form': profile_form} )

def user_login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('instrument_list')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'blog/login.html', {})

@login_required
def user_settings(request):

    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save()
            profile.save()
            return redirect('instrument_list')

        # Invalid form or forms - mistakes or something else? Print problems to the terminal. They'll also be shown to the user.
        else:
            print(profile_form.errors)
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'blog/user_settings.html', {'profile_form': profile_form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # If you uncomment the line below, you aren't logged out when you change your password
            update_session_auth_hash(request, form.user)
            return redirect('instrument_list')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'blog/password_change.html', {'form': form})

@login_required
def user_logout_confirm(request):
    return render(request, 'blog/logout_confirm.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('instrument_list')

@login_required
def instrument_close_connection(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if instrument.instrument_current_owner != request.user:
        error = "not current owner"
        return render(request, 'blog/not_today.html', {'error': error})
    elif instrument.instrument_connection == False:
        error = "not connected to server"
        return render(request, 'blog/not_today.html', {'error': error})
    else:
        if request.method == "POST":
            form = InstrumentConnectionForm(request.POST, instance=instrument)
            if form.is_valid():
                instrument = form.save(commit=False)
                instrument.instrument_connection = False
                form.save()
                return redirect('instrument_list')
            else:
                print(form.errors)

        else:
            form = InstrumentConnectionForm(instance=instrument)
        return render(request, 'blog/instrument_close_connection.html', {'form': form})

@login_required
def instrument_open_connection(request, pk):
    instrument = get_object_or_404(Instrument, pk=pk)
    if instrument.instrument_current_owner == request.user:
        if request.method == "POST":
            form = InstrumentConnectionForm(request.POST, instance=instrument)
            if form.is_valid():
                instrument = form.save(commit=False)
                instrument.instrument_connection = True
                form.save()
                return redirect('instrument_list')
            else:
                print(form.errors)

        else:
            form = InstrumentConnectionForm(instance=instrument)
        return render(request, 'blog/instrument_open_connection.html', {'form': form})
    else:
        return render(request, 'blog/not_today.html')

@login_required
def user_message (request, pk):
    user = User.objects.get(pk=pk)
    user_name = user.profile.get_full_name()
    if request.method == "POST":
        form = UserMessageForm(request.POST)
        if form.is_valid():
            recipient_list = []
            subject_line = "RAM message from " + str(request.user.profile.first_name) + " " + str(request.user.profile.last_name)
            message_text = form.cleaned_data['message']
            if user.profile.email:
                    recipient_list.append(user.profile.email)
            if user.profile.mobile_number:
                    sms_email = user.profile.mobile_number + user.profile.mobile_carrier
                    recipient_list.append(sms_email)
            if recipient_list:
                massMessageSend.delay(subject_line, message_text, recipient_list)
            return redirect('instrument_list')
    else:
        form = UserMessageForm()
    return render(request, 'blog/user_message.html', {'form': form, 'user_name': user_name})