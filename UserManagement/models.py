from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserDetail(models.Model):
    ROLES = (('MECHANIC', 'Mechanic'), ('CUSTOMER', 'Customer'))
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    role = models.CharField(max_length=20,choices=ROLES)
    contact = models.IntegerField()

    def __str__(self):
        return self.user.username


