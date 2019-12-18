from django.db import models
from UserManagement.models import UserDetail

# Create your models here.
class Garage(models.Model):
    owner = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    address = models.TextField()
    garage_name=models.CharField(max_length=50)
    city = models.CharField(max_length=20, null=True)
    contact = models.IntegerField(null=True)
    lat = models.FloatField()
    longi = models.FloatField()
    # otp
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.garage_name

class Otp(models.Model):
    otp=models.CharField(max_length=6)
    contact = models.IntegerField(null=False)
    is_verified = models.BooleanField(default=False)
