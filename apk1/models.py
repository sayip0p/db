from django.db import models
class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    phone=models.IntegerField()

class Product(models.Model):
    name= models.CharField(max_length=100)
    brand= models.CharField(max_length=100)
    price= models.IntegerField()
    image= models.FileField(upload_to='products',blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    def str(self):
        return f"Rating: {self.rating}, feedback: {self.feedback_text[:50]}..."
    
class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet')
    ], default='card')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('success', 'success'), ('failed', 'failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"payment of {self.amount} by {self.email} - {self.status}"

class staff_login(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_id

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')
    stock_status = models.CharField(max_length=20, choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')])
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class yemani_login(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_id
    
class YemaniFoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')
    stock_status = models.CharField(
        max_length=20,
        choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')]
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
