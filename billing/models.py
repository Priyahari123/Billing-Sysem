from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    available_stock = models.IntegerField()
    unit_price = models.FloatField()
    tax_percentage = models.FloatField()

    def __str__(self):
        return self.name
    

class Denomination(models.Model):
    value = models.IntegerField(unique=True)
    available_count = models.IntegerField()

    def __str__(self):
        return str(self.value)



class Customer(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    total_tax = models.FloatField()
    net_price = models.FloatField()
    paid_amount = models.FloatField()
    balance_amount = models.FloatField()
    is_bill_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()