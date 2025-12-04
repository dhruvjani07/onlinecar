from django.contrib import admin
from .models import Vehicle, Favorite


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Admin interface for Vehicle model"""
    list_display = ['title', 'company', 'model', 'year', 'price', 'condition', 'seller', 'is_sold', 'is_featured', 'created_at']
    list_filter = ['category', 'fuel_type', 'transmission', 'condition', 'is_sold', 'is_featured', 'created_at']
    search_fields = ['title', 'company', 'model', 'city']
    list_editable = ['is_featured', 'is_sold']
    readonly_fields = ['created_at', 'updated_at', 'estimated_price']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'model', 'year')
        }),
        ('Technical Details', {
            'fields': ('category', 'fuel_type', 'transmission', 'mileage', 'condition')
        }),
        ('Pricing', {
            'fields': ('original_price', 'price', 'estimated_price')
        }),
        ('Description', {
            'fields': ('description', 'features')
        }),
        ('Location', {
            'fields': ('city',)
        }),
        ('Seller', {
            'fields': ('seller', 'seller_phone')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3', 'image4')
        }),
        ('Status', {
            'fields': ('is_sold', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin interface for Favorite model"""
    list_display = ['user', 'vehicle', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'vehicle__title']
    date_hierarchy = 'created_at'