from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_table(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pincode=models.IntegerField()
    district=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class contractor_table(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    dob=models.DateField()
    gender=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    address=models.CharField(max_length=100)
    photo=models.ImageField()
    proof=models.ImageField()
    status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class shop_table(models.Model):
    name=models.CharField(max_length=100)
    owner_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pincode=models.IntegerField()
    district=models.CharField(max_length=100)
    photo=models.ImageField()
    proof=models.ImageField()
    status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class category_table(models.Model):
    category_name=models.CharField(max_length=100)

class complaint_table(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=500)
    reply=models.CharField(max_length=500)
    status=models.CharField(max_length=100)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class product_table(models.Model):
    item_name=models.CharField(max_length=100)
    price=models.IntegerField()
    photo=models.ImageField()
    details=models.CharField(max_length=300)
    SHOP=models.ForeignKey(shop_table,on_delete=models.CASCADE)  

class work_table(models.Model):
    work_name=models.CharField(max_length=100)
    photo=models.ImageField()
    description=models.CharField(max_length=300)
    rate=models.IntegerField()
    CONTRACTOR=models.ForeignKey(contractor_table,on_delete=models.CASCADE) 

class request_table(models.Model):
    date=models.DateField()
    status=models.CharField(max_length=100)
    WORK=models.ForeignKey(work_table,on_delete=models.CASCADE)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
     
class offer_table(models.Model):
    date_entry=models.DateField()
    start_date=models.DateField()
    end_date=models.DateField()     
    offer_name=models.CharField(max_length=100)
    offer_price=models.IntegerField()
    details=models.CharField(max_length=300)
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)


class review_table(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=500)
    rating=models.FloatField()
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class cart_table(models.Model):
    date=models.DateField() 
    quantity=models.IntegerField()
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)
    lOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
   


class order_main_table(models.Model):
    date=models.DateField() 
    total_amount=models.IntegerField()
    status=models.CharField(max_length=100)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class order_sub_table(models.Model):
    ORDER_MAIN=models.ForeignKey(order_main_table,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    PRODUCT=models.ForeignKey(product_table,on_delete=models.CASCADE)

# class assign_table(models.Model):
#     date=models.DateField() 
#     status=models.CharField(max_length=100)
#     ORDER_MAIN=models.ForeignKey(order_main_table,on_delete=models.CASCADE)

class payment_table(models.Model):
    date=models.DateField() 
    total_amount=models.IntegerField()
    status=models.CharField(max_length=100)
    ORDER_MAIN=models.ForeignKey(order_main_table,on_delete=models.CASCADE)


class return_product_table(models.Model):
        date=models.DateField() 
        USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
        reason=models.CharField(max_length=300)
        ORDER_MAIN=models.ForeignKey(order_main_table,on_delete=models.CASCADE)
        status=models.CharField(max_length=100)
        photo=models.ImageField()

class worker_review(models.Model):
     date=models.DateField() 
     review=models.CharField(max_length=300)
     rating=models.FloatField()
     REQUEST=models.ForeignKey(request_table,on_delete=models.CASCADE)
     USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class feedback_table(models.Model):
     date=models.DateField() 
     feedback=models.CharField(max_length=300)
     rating=models.FloatField()
     USER=models.ForeignKey(user_table,on_delete=models.CASCADE)









