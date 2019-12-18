from django.shortcuts import render
from django.contrib.auth.models import User
from UserManagement.models import UserDetail
from garage.models import Garage,Otp
from django.http import JsonResponse
import json
from django.conf import settings
import requests
from django.utils.crypto import get_random_string

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

    user=User.objects.create(first_name=first_name,last_name=last_name,username=username,is_active=False)
    user.set_password(password)
    user.save()

    garage_owner = UserDetail.objects.create(contact=contact,address=address,role=role,user=user)

    garage=Garage.objects.create(garage_name=garage_name,city=city,
        lat=lat,longi=longi,owner=garage_owner)

    otp_sent = send_otp(contact)
    if otp_sent:
        return JsonResponse({'response':'Otp sent successfully'})
    else:
        return JsonResponse({'response':'Internal server issue. Please try after sometime.'})


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

def verify_otp(request):
    data = json.loads(request.body)
    contact = data.get"(contact")
    otp = data.get("otp")

    instance = Otp.objects.filter(contact=contact,is_verified=False).last()

    if not instance:
        return JsonResponse({"response":"Internal server error" })

    if otp.strip() == instance.otp.strip():
        instance.is_verified = True
        instance.save()

        try:
            garage= Garage.objects.get(contact=contact,is_active=False)
            garage.is_active=True
            garage.owner.user.is_active=True
            garage.owner.user.save()
            garage.save()
            return JsonResponse({"response":"User registered successfully" })

        except Exception as e:
            return JsonResponse({"response":"Not found" })




def send_otp(contact):
    otp = get_random_string(length=6, allowed_chars='1234567890')
    params ={
              "sender_id": "FSTSMS",
              "message": str(otp),
              "numbers": str(contact),
              "language": "english",
              "route": "p"
              }
    response = requests.post(settings.SMS_URL,params=params,headers={'authorization': settings.SMS_API_KEY})
    content = response.json()
    if contact.get("return"):
        otp = Otp.objects.create(otp=otp,contact=contact)
        return True
    else:
        return False
