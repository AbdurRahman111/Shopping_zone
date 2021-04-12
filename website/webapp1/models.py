from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
# Create your models here.


class EmailConfirmed(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key=models.CharField(max_length=500)
    email_confirmed=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='User Email-Confirmed'

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance=EmailConfirmed(user=instance)
        user_encoded=f'{instance.email}-{dt}'.encode()
        activation_key=hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key=activation_key
        email_confirmed_instance.save()



class Categories(models.Model):
    category_name=models.CharField(max_length=500)

    def __str__(self):
        return self.category_name


class products(models.Model):
    product_name = models.CharField(max_length=2000)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_price = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='uploads/product_image')
    image2 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image3 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image4 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image5 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    description = models.TextField()

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=1000)
    product_details = models.TextField()
    total_bill = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    country = models.CharField(max_length=1000)
    street = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    zip = models.CharField(max_length=1000)
    ordered = models.BooleanField(default=False)
    order_date = models.DateField(default=datetime.now(), blank=True)


class contact_us(models.Model):
    email=models.CharField(max_length=200)
    message=models.TextField()

    def __str__(self):
        return self.email