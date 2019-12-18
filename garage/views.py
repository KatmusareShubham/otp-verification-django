from django.shortcuts import render
from django.contrib.auth.models import User
from UserManagement.models import UserDetail
from garage.models import Garage
from django.http import JsonResponse
import json

from django.contrib.auth import login, authenticate, logout

# Create your views here.
def Create_garage_With_owner(request):
    data = json.loads(request.body)

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password','')

    confirm_password = data.get('confirm_password','')

    if password.strip() != confirm_password.strip():
            return JsonResponse({'response': 'Password do not matched'})

    if UserDetail.objects.filter(user__username = username):
        return JsonResponse({'response': 'username already exists'})

    role = data.get('role')
    address = data.get('address')
    contact = data.get('contact')

    garage_name = data.get('garage_name')
    city = data.get('city')
    lat = data.get('lat')
    longi = data.get('longi')

    user=User.objects.create(first_name=first_name,last_name=last_name,username=username)
    user.set_password(password)
    user.save()

    garage_owner = UserDetail.objects.create(contact=contact,address=address,role=role,user=user)

    garage=Garage.objects.create(garage_name=garage_name,city=city,
        lat=lat,longi=longi,owner=garage_owner)

    return JsonResponse({'response':'Garage owner registered successfully'})


def garage_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user=authenticate(username=username,password=password)

    if not user:
        return JsonResponse({"response":"Wrong credentials"})

    if not user.is_active:
        return JsonResponse({"response": "INVALID account"})
    # print("user is active ", True)
    login(request,user)
    return JsonResponse({"response": "LOG in successfully"})

def get_garage(request):
    data = json.loads(request.body)
    add = data.get('Address')
    garage_list=[]
    garage_queryset=Garage.objects.filter(address=add)

    return JsonResponse({"response": garage_list})

