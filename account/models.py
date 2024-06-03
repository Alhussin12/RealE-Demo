from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userphoto=models.ImageField(upload_to ='photos/%Y/%m/%d/' ,null=True)
    address = models.CharField(max_length=60)
    address2= models.CharField(max_length=60)
    city= models.CharField(max_length=60)
    state= models.CharField(max_length=60)
    zip_number= models.CharField(max_length=60)
    isvarifaied=models.BooleanField(default=False)
    code =models.DecimalField(max_digits=4,decimal_places=0,default=0000)
    def __str__(self):
        return self.user.username