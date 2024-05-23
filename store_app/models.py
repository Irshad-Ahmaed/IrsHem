from django.utils import timezone
import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
     
class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# class Sizes(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    Filter_Price = (
        ('200 To 500' , '200 To 500' ),
        ('500 To 1000' , '500 To 1000' ),
        ('1000 To 1500' , '1000 To 1500' ),
        ('1500 To 2000' , '1500 To 2000' ),
        ('2000 To 3000' , '2000 To 3000' ),
    )
    price = models.CharField(choices=Filter_Price,max_length=60)

    def __str__(self):
        return self.price

class Product(models.Model):
    CONDITION = (('New', 'New'),('Old', 'Old'))
    STOCK = (('In Stock', 'In Stock'),('Out of Stock', 'Out of Stock'))
    STATUS = (('Publish', 'Publish'),('Draft', 'Draft'))
    
    unique_id = models.CharField(unique=True,max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='Product_image/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION,max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK,max_length=200)
    status = models.CharField(choices=STATUS ,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # sizes = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price*100)


class Photo(models.Model):
    image = models.ImageField(upload_to='Product_image/img')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Tags(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length =100)
    lastname = models.CharField(max_length =100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    amount = models.CharField(max_length=100)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.user.username
    

ORDERSTATUS = ((1, "Pending"), (2,"Dispatch"), (3,"On the way"), (4,"Arrived in City"), (5,"Delivered"))

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    userDetail = models.EmailField(Order, max_length=100)
    status = models.IntegerField(choices=ORDERSTATUS, default=1)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Product_Image/Order_Img")
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)
    created = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return self.order.user.username
    
class Product_review(models.Model):
    prod_id = models.CharField(max_length=200)
    name = models.CharField(max_length =100)
    email = models.EmailField(Order, max_length=100)
    reviewMessage = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.email