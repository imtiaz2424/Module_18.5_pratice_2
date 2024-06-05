from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():            
            messages.success(request, 'Account Created Successfully')
            register_form.save()
            return redirect('profile')
    else:
        register_form = forms.RegistrationForm(request.POST)
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                messages.success(request, 'Logged In Successfully')
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, 'Login information incorrect')
                return redirect('register')
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form': form, 'type' : 'Login'})


@login_required
def profile(request):       
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
       profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
       if profile_form.is_valid():            
            messages.success(request, 'Profile Updated Successfully')
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'update_profile.html', {'form' : profile_form})


# password change with old password
def pass_change(request):
    if request.method == 'POST':
        pass_change_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_change_form.is_valid():            
            messages.success(request, 'Password Updated Successfully')
            pass_change_form.save()
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('profile')
    else:
        pass_change_form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : pass_change_form})

# password change without old password
def pass_change_without(request):
    if request.method == 'POST':
        pass_change_form = SetPasswordForm(request.user, data=request.POST)
        if pass_change_form.is_valid():            
            messages.success(request, 'Password Updated Successfully')
            pass_change_form.save()
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('profile')
    else:
        pass_change_form = SetPasswordForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : pass_change_form})




def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('homepage')