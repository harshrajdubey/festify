from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import User
from .forms import RegisterForm, LoginForm, OTPVerificationForm
import json

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate OTP for phone verification
            otp = user.generate_phone_otp()
            # Store user ID in session for OTP verification
            request.session['user_id'] = user.id
            request.session['phone_number'] = user.phone_number
            
            # TODO: Send OTP via SMS (for now, we'll just show it in messages)
            messages.success(request, f'Registration successful! OTP sent to {user.phone_number}. OTP: {otp}')
            return redirect('users:verify_otp')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    if user.is_verified:
                        # User is verified, log them in
                        request.session['user_id'] = user.id
                        messages.success(request, 'Login successful!')
                        return redirect('users:profile', username=user.username)
                    else:
                        # User not verified, send new OTP
                        otp = user.generate_phone_otp()
                        request.session['user_id'] = user.id
                        request.session['phone_number'] = user.phone_number
                        messages.info(request, f'Please verify your phone number. OTP sent: {otp}')
                        return redirect('users:verify_otp')
                else:
                    messages.error(request, 'Invalid username or password')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('users:register')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if user.verify_phone_otp(otp):
                messages.success(request, 'Phone number verified successfully!')
                return redirect('users:profile', username=user.username)
            else:
                messages.error(request, 'Invalid or expired OTP')
    else:
        form = OTPVerificationForm()
    
    # Check if user can resend OTP
    can_resend, resend_message = user.can_resend_otp()
    
    return render(request, 'users/verify_otp.html', {
        'form': form, 
        'phone_number': user.phone_number,
        'can_resend': can_resend,
        'resend_message': resend_message if not can_resend else None,
        'resend_count': user.otp_resend_count
    })

def resend_otp(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'Session expired'})
        
        user = get_object_or_404(User, id=user_id)
        otp, message = user.resend_otp()
        
        if otp:
            # TODO: Send OTP via SMS (for now, we'll just show it in the response)
            return JsonResponse({
                'success': True, 
                'message': f'{message} New OTP: {otp}',
                'resend_count': user.otp_resend_count
            })
        else:
            return JsonResponse({'success': False, 'message': message})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    logged_in_user_id = request.session.get('user_id')
    
    # Check if user is verified and logged in
    if not logged_in_user_id or logged_in_user_id != user.id:
        messages.error(request, 'Please login to access this page')
        return redirect('users:login')
    
    if not user.is_verified:
        messages.error(request, 'Please verify your phone number first')
        return redirect('users:verify_otp')
    
    return render(request, 'users/profile.html', {'user': user})

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('users:login')
