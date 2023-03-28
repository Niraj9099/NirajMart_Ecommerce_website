from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    village = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)
    


CATEGOTY_CHOICES = (
    ('M', 'MOBILE'),
    ('L', 'LAPTOP'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discription = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGOTY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def Cart_total(self):
        return self.quantity * self.product.discount_price



STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
class OrderPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')

    @property
    def Order_total(self):
        return self.quantity * self.product.discount_price
