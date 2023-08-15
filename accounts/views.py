from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from .models import LoginUserInfo
import uuid

def account(request):
    return render(request, "account.html")

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        form_data = request.POST.dict()

        # Access the form data
        email = form_data.get('email')
        password = form_data.get('password')
        
        # Authenticate user
        User = get_user_model()
        try:
            # Match email with the user model
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response_data = {
                'result': 'Invalid email or password'
            }
            return JsonResponse(response_data, status=400)

        # Check if the password matches
        if user.check_password(password):
            # Login the user
            login(request, user)
            # Save additional user info in the UserInfo model
            user_info = LoginUserInfo.objects.create(
                user=user,
                email=email,
                session=request.session.session_key,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            response_data = {
                'result': 'SignIn Successful'
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'result': 'Invalid email or password'
            }
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def signout(request):
    logout(request)
    return redirect('account')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        payload = json.loads(form_data.get('payload'))

        # Access the form data        
        first_name=form_data.get('first_name')
        last_name=form_data.get('last_name')
        email = form_data.get('email')
        password = form_data.get('password')

        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            response_data = {
                'result': 'Email already exists'
            }
            return JsonResponse(response_data, status=400)
        
        # Generate a unique and small username
        username = f"{first_name.lower()}{last_name.lower()}"
        # Truncate the username to a desired length, e.g., 8 characters
        max_length = 8
        username = username[:max_length]
        while User.objects.filter(username=username).exists():
            username += uuid.uuid4().hex[:4]

        # print("username,first_name,last_name,email,password:::::::::::::",username,first_name,last_name,email,password,request.session.session_key,request.META.get('REMOTE_ADDR'))

        # Save user data in the User model
        user = User.objects.create_user(
            username=username, 
            first_name=first_name,
            last_name=last_name,
            email=email, 
            password=password,
            # session=request.session.session_key if(request.session.session_key == None) else "",
            # ip_address=request.META.get('REMOTE_ADDR')
        )

        response_data = {
            'result':"SignUp Successful"
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)