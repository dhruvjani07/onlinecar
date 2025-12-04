from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Vehicle(models.Model):
    """Vehicle model for car listings"""
    
    CATEGORY_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('truck', 'Truck'),
        ('coupe', 'Coupe'),
        ('van', 'Van'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=50, verbose_name="Car Company")
    model = models.CharField(max_length=50)
    year = models.IntegerField(verbose_name="Manufacturing Year")
    
    # Technical Details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sedan')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    mileage = models.IntegerField(help_text="Mileage in kilometers")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original purchase price")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Current Selling Price")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Estimated Price")
    
    # Description
    description = models.TextField()
    features = models.TextField(blank=True, help_text="One feature per line")
    
    # Location
    city = models.CharField(max_length=100)
    
    # Seller Information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    seller_phone = models.CharField(max_length=20)
    
    # Images
    image1 = models.ImageField(upload_to='vehicles/', default='default.jpg')
    image2 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image3 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image4 = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    
    # Status
    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
    
    def __str__(self):
        return f"{self.year} {self.company} {self.model}"
    
    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'pk': self.pk})


class Favorite(models.Model):
    """User favorites/wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'vehicle']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.vehicle}"
    

class Order(models.Model):
    """Model for online car purchases - INSTANT SALE ON COD"""
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Debit/Credit Card'),
    ]
    
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Buyer Details (collected at order time)
    buyer_full_name = models.CharField(max_length=200)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=20)
    
    # Delivery Address
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_postal_code = models.CharField(max_length=20)
    
    # Payment Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Card Details (stored for admin reference only)
    card_number = models.CharField(max_length=19, blank=True)
    card_name = models.CharField(max_length=100, blank=True)
    card_expiry = models.CharField(max_length=7, blank=True)
    
    # Order Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.vehicle.title} by {self.buyer.username}"