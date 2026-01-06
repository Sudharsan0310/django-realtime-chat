from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import *

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'a_users/profile.html', {'profile':profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)  
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False
      
    return render(request, 'a_users/profile_edit.html', { 'form':form, 'onboarding':onboarding })


@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Send confirmation email using new method
            try:
                email_address = EmailAddress.objects.get_for_user(request.user, email)
                if email_address:
                    email_address.send_confirmation(request)
                    messages.success(request, 'Confirmation email sent!')
            except EmailAddress.DoesNotExist:
                # Create email address if it doesn't exist
                email_address = EmailAddress.objects.add_email(
                    request, 
                    request.user, 
                    email, 
                    confirm=True
                )
                messages.success(request, 'Confirmation email sent!')
            except Exception as e:
                messages.warning(request, 'Email updated but confirmation email could not be sent.')
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Email not valid or already in use')
            return redirect('profile-settings')
        
    return redirect('profile-settings')


@login_required
def profile_usernamechange(request):
    if request.htmx:
        form = UsernameForm(instance=request.user)
        return render(request, 'partials/username_form.html', {'form':form})
    
    if request.method == 'POST':
        form = UsernameForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Username updated successfully.')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Username not valid or already in use')
            return redirect('profile-settings')
    
    return redirect('profile-settings')    


@login_required
def profile_emailverify(request):
    # Send verification email using new method
    try:
        email_address = EmailAddress.objects.get_primary(request.user)
        if email_address and not email_address.verified:
            email_address.send_confirmation(request)
            messages.success(request, 'Verification email sent!')
        elif email_address and email_address.verified:
            messages.info(request, 'Email is already verified.')
        else:
            messages.warning(request, 'No email address found.')
    except Exception as e:
        messages.error(request, 'Could not send verification email.')
    
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'a_users/profile_delete.html')