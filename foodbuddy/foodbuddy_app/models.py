from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.core.validators import RegexValidator,MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class UserDetail(models.Model):
    '''
    Model to represent a table to store user details.
    '''
    class Meta:
        permissions = [
            ("isUser", "Regular System User"),
            ("isRestaurant", "Restaurant Admin"),
        ]
    #     db_table = 'tomato_user'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    UID = models.AutoField(primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?(91)?\d{9,10}$', message="Phone number must be entered in the format: '(+91)9999999999'. +91 is optional.")
    Phone_No = models.CharField(validators=[phone_regex], max_length=13,null=False, blank=False) # validators should be a list
    Address=models.CharField(null=False, blank=False,max_length=500)
    Type=models.CharField(null=False, blank=False,max_length=1,default="U") # U-User R-restaurant
    def __str__(self):
        return str(self.UID)

class Restaurant(models.Model):
    '''
    Model to represent a table to store restaurant details. 
    '''
    # class Meta:
    #     db_table = 'tomato_restaurant'
    RID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    Name=models.CharField(null=False, blank=False,max_length=50)
    
    phone_regex = RegexValidator(regex=r'^\+?(91)?\d{9,10}$', message="Phone number must be entered in the format: '(+91)9999999999'. +91 is optional.")
    Phone_No = models.CharField(validators=[phone_regex], max_length=13,null=False, blank=False) # validators should be a list
    Address=models.CharField(null=False, blank=False,max_length=500)

    # Type=models.CharField(null=False, blank=False,max_length=1)
    Rating_Cnt= models.IntegerField(default=0)
    Rating= models.DecimalField(decimal_places=2,max_digits=5,default=0.0)
    # Lat=models.FloatField(null=False, blank=False)
    # Long=models.FloatField(null=False, blank=False)
    Image=models.ImageField(upload_to='images/',null=True, blank=True)
    Type=models.CharField(null=False, blank=False,max_length=1,default="R")

    def __str__(self):
        return str(self.RID)

class Bookings(models.Model):
    '''
    Model to represent a table to store details for a booking.
    '''
    class Meta:
        unique_together = (('BID','RID','UID'),)
    BID=models.AutoField(primary_key=True)
    RID=models.ForeignKey(Restaurant, on_delete=models.CASCADE,db_column="RID")
    UID=models.ForeignKey(UserDetail, on_delete=models.CASCADE,db_column="UID")
    Start_Date=models.DateField(null=False, blank=False)
    End_Date=models.DateField(null=False, blank=False)
    Start_Time=models.TimeField(null=False, blank=False)
    End_Time=models.TimeField(null=False, blank=False)
    Party=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    Name=models.CharField(blank=True,max_length=50)
    Descrip=models.CharField(blank=True,max_length=500)
    Rating= models.DecimalField(null=True, blank=True,decimal_places=2,max_digits=5)
    # Status=models.BooleanField(null=False, blank=False)
    Status=models.CharField(null=False,max_length=1,default="S") #A-accepted R-Rejected S-Submitted M-modified
    def __str__(self):
        return str(self.RID)+" "+str(self.UID)

#Unused models-
# class Prices(models.Model):
#     # class Meta:
#     #     db_table = 'tomato_restaurant'
#     PID=models.AutoField(primary_key=True)
#     RID=models.ForeignKey(Restaurant, on_delete=models.CASCADE,db_column="RID")
#     Service=models.CharField(null=False, blank=False,max_length=1)
#     Price=models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False)
#     def __str__(self):
#         return str(self.RID)+" "+str(self.PID)
# Due to Composite Primary Key not working properly hence not registering these models with admin
# class Restaurant_Item(models.Model):
#     class Meta:
#         unique_together = (('RID','IID'),)
#         # db_table = 'tomato_restaurant_item'
#     id=models.AutoField(primary_key=True)
#     RID=models.ForeignKey(Restaurant, on_delete=models.CASCADE,db_column="RID")
#     IID=models.IntegerField(null=False, blank=False)
#     Name=models.CharField(null=False, blank=False,max_length=50)
#     Description=models.CharField(null=False, blank=False,max_length=500)
#     Image=models.ImageField(upload_to='images/',null=False, blank=False)
#     Price=models.DecimalField(decimal_places=2,max_digits=10,null=False, blank=False)
#     Category=models.CharField(null=False, blank=False,max_length=1)
#     def __str__(self):
#         return str(self.RID)+"_"+str(self.IID)

# class Order(models.Model):
#     # class Meta:
#     #     db_table = 'tomato_order'
#     OID=models.IntegerField(primary_key=True)
#     UID=models.ForeignKey(User, on_delete=models.CASCADE,db_column="UID")
#     RID=models.ForeignKey(Restaurant, on_delete=models.CASCADE,db_column="RID")
#     EID=models.ForeignKey(Employee, on_delete=models.CASCADE,db_column="EID")
#     Status=models.CharField(null=False, blank=False,max_length=1)
#     Lat=models.FloatField(null=False, blank=False)
#     Long=models.FloatField(null=False, blank=False)
#     def __str__(self):
#         return str(self.OID)

# class Delivery_Item(models.Model):
#     class Meta:
#         unique_together = (('OID','RID','IID'),)
#         # db_table = 'tomato_delivery_item'
#     OID=models.ForeignKey(Order, on_delete=models.CASCADE,db_column="OID")
#     RID=models.ForeignKey(Restaurant, on_delete=models.CASCADE,db_column="RID")
#     IID=models.ForeignKey(Restaurant_Item, on_delete=models.CASCADE,db_column="IID")
#     Qty=models.IntegerField(null=False, blank=False)
#     def __str__(self):
#         return str(self.OID)

# class Employee(models.Model):
#     # class Meta:
#     #     db_table = 'tomato_employee'
#     EID = models.AutoField(primary_key=True)
#     Name=models.CharField(null=False, blank=False,max_length=50)
#     Email=models.EmailField(null=False, blank=False)
#     phone_regex = RegexValidator(regex=r'^\+?(91)?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
#     Phone_No = models.CharField(validators=[phone_regex], max_length=13,null=False, blank=False) # validators should be a list
#     Address=models.CharField(null=False, blank=False,max_length=500)
#     def __str__(self):
#         return str(self.EID)