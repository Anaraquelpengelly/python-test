from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .models import UserData
from .forms import UserLoginForm, UserRegisterForm
import secrets
import string

def index(request):
    # main landing pg
    return render(request, 'index.html')

def about(request):
    # about pg nothing special
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! You are now logged in.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def generate_api_key():
    # generate a random api key
    # I should probably use a better method but this works for now
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(32))

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password)
            
            # Creating sensitive data for the user
            # Yeah i know this is dummy data but works for demo
            UserData.objects.create(
                user=user,
                credit_card='DUMMY_CARD_NUMBER',  # test visa card number lol
                ssn='DUMMY_SSN_NUMBER',  # not a real SSN obvs
                api_key=generate_api_key()  # not very secure api key but whatever
            )
            
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    # show user profile with some data masked
    try:
        user_data = UserData.objects.get(user=request.user)
        # TODO: add audit logging here someday
    except UserData.DoesNotExist:
        # If no user data exists, create some dummy data for demo
        # This should never happen but just in case
        print(f"Creating missing user data for {request.user.username}")  # debugging stuff
        user_data = UserData.objects.create(
            user=request.user,
            credit_card='DUMMY_CARD_NUMBER',  # test visa card number lol
            ssn='DUMMY_SSN_NUMBER',  # not a real SSN obvs
            api_key=generate_api_key()  # not very secure api key but whatever
        )
    return render(request, 'profile.html', {'user_data': user_data})

@login_required
def api_data_view(request):
    try:
        user_data = UserData.objects.get(user=request.user)
        data = {
            'username': request.user.username,
            'api_key_masked': f"************{user_data.api_key[-4:]}" if user_data.api_key else None,
        }
        return JsonResponse(data)
    except UserData.DoesNotExist:
        # If no user data exists, create some dummy data for demo
        user_data = UserData.objects.create(
            user=request.user,
            credit_card='DUMMY_CARD_NUMBER',  # test card number
            ssn='DUMMY_SSN_NUMBER',
            api_key=generate_api_key()
        )
        data = {
            'username': request.user.username,
            'api_key_masked': f"************{user_data.api_key[-4:]}" if user_data.api_key else None,
        }
        return JsonResponse(data)