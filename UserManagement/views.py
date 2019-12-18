from django.shortcuts import render
from django.http import JsonResponse
import json
from UserManagement.models import UserDetail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def user_registration(request):
    data = json.loads(request.body)

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    contact = data.get('contact')
    address = data.get('address')
    password = data.get('password','')
    confirm_password = data.get('confirm_password','')
    role = data.get('role')

    if password.strip() != confirm_password.strip():
        return JsonResponse({'response': 'Password do not matched'})

    if UserDetail.objects.filter(user__username = username):
        return JsonResponse({'response': 'username already exists'})

    user = User.objects.create(first_name=first_name,last_name=last_name,username=username)
    user.set_password(password)
    user.save()

    userdetails = UserDetail.objects.create(contact=contact,address=address,role=role,user=user)

    return JsonResponse({'response':'USER registered successfully'})


def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({"response":"Wrong credentials"})

    if not user.is_active:
        return JsonResponse({"response": "INVALID account"})
    print("user", user)
    login(request, user)
    return JsonResponse({"response": "LOG in successfully"})


