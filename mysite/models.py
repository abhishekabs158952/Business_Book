from django.db import models

class userCredentials(models.Model):
    userName = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=14)
    address = models.IntegerField()
    email = models.EmailField()
    #password = models.CharField(max_length=30)
    class Meta:
        db_table ="customerdetails"

class originalUserCredentials(models.Model):
    userName = models.CharField(primary_key=True,max_length=30)
    password = models.CharField(max_length=30)    
    userType = models.CharField(max_length=1)
    class Meta:
        db_table ="userCredentials"

class sellerdetials(models.Model):
    userName = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=14)
    address = models.IntegerField()
    email = models.EmailField()
    #password = models.CharField(max_length=30)
    typeOfShop = models.CharField(max_length=30)
    shopName = models.CharField(max_length=30)
    class Meta:
        db_table ="sellerDetails"

class addStock(models.Model):
    itemId = models.BigAutoField(primary_key=True)
    itemName = models.CharField(max_length=30)
    sellerId = models.CharField(max_length=30)
    itemStock = models.IntegerField()
    cost = models.IntegerField()
    sellerPrice = models.IntegerField()
    customerPrice = models.IntegerField()
    class Meta:
        db_table ="stock"
    
class transection(models.Model):
    id = models.BigAutoField(primary_key=True)
    sellerId =models.CharField(max_length=30)
    customerId =models.CharField(max_length=30)
    dateTime =models.DateTimeField()
    totalAmount =models.IntegerField()
    orderStatus =models.IntegerField()
    class Meta:
        db_table="transection"

class transectionId(models.Model):     
    id = models.BigAutoField(primary_key=True)
    transectionId =models.BigIntegerField()
    itemId=models.IntegerField()  
    quantity =models.IntegerField()
    price=models.IntegerField()
    total=models.IntegerField()
    class Meta:
        db_table="transectionId"

class chatTable(models.Model):     
    id = models.BigAutoField(primary_key=True)
    transectionId = models.BigIntegerField()
    sellerId = models.CharField(max_length=30)
    customerId = models.CharField(max_length=30)
    dateTime = models.DateTimeField()
    message = models.CharField(max_length=500)
    sender = models.CharField(max_length=30)
    class Meta:
        db_table="chat_table"

class userPhoto(models.Model):
    userName = models.CharField(primary_key=True,max_length=30)
    photo = models.ImageField(upload_to = 'Image/')
