from statistics import mode
from django.db import models
from account.models import User
from django.utils.translation import gettext as _
class proerities(models.Model):
    rel=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name
class proeritie(models.Model):
    rs={('Rent','re'),('Sell','se')}
    date=models.CharField(_("date") ,null=True,max_length=255)
    price=models.DecimalField(_("price"),null=True,max_digits=30,decimal_places=0)
    bedrooms=models.DecimalField(_("bedrooms"),max_digits=2,decimal_places=0,null=True)
    bathrooms=models.DecimalField(_("bathrooms"),max_digits=4,decimal_places=2,null=True)
    sqft_living=models.DecimalField(_("sqft living"),max_digits=5,decimal_places=0,null=True)
    sqft_lot=models.DecimalField(_("sqft lot"),max_digits=7,decimal_places=0,null=True)
    floors=models.DecimalField(_("floors"),max_digits=4,decimal_places=2,null=True)
    waterfront=models.DecimalField(_("waterfront"),max_digits=1,decimal_places=0,null=True)
    view=models.DecimalField(_("view"),max_digits=1,decimal_places=0,null=True)
    condition=models.DecimalField(_("condition"),max_digits=1,decimal_places=0,null=True)
    grade=models.DecimalField(_("grade"),max_digits=2,decimal_places=0,null=True)
    sqft_above=models.DecimalField(_("sqft above"),max_digits=4,decimal_places=0,null=True)
    sqft_basement=models.DecimalField(_("sqft basement"),max_digits=4,decimal_places=0,null=True)
    yr_built=models.TextField(_("yr built"),max_length=4,null=True)
    yr_renovated=models.TextField(_("yr built"),max_length=4,null=True)
    zipcode=models.DecimalField(_("zipcode"),max_digits=6,decimal_places=0,null=True)
    lat=models.DecimalField(_("lat"),max_digits=20,decimal_places=16,null=True)
    long=models.DecimalField(_("long"),max_digits=20,decimal_places=16,null=True)
    sqft_living15=models.DecimalField(_("sqft livingfif"),max_digits=4,decimal_places=0,null=True)
    sqft_lot15=models.DecimalField(_("sqft livingfif"),max_digits=7,decimal_places=0,null=True)
    title=models.TextField(null=True,max_length=255)
    photo=models.ImageField(upload_to ='photos/%Y/%m/%d/',null=True)
    rel=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='Owne')
    type=models.CharField(choices=rs ,null=True,max_length=50)
    is_check=models.BooleanField(default=True)
    def __str__(self):
        return  str(self.id) +"  "+str(self.title)