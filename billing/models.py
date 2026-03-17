from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    product_id=models.IntegerField(unique=True)
    available_stocks=models.IntegerField()
    price=models.FloatField()
    tax =models.FloatField()

    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    customer_email=models.EmailField()
    total_amount=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_email

class PurchaseItem(models.Model):
    purchase=models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.FloatField()

    def __str__(self):
        return f"{self.product.product_id}-{self.product.name}"
    





