from django import forms
from datetime import date
from .models import Vehicle, Favorite, Order
from vehicle_utils import VehicleValidator


class VehicleForm(forms.ModelForm):
    """Form for creating and editing vehicles"""
    
    # Add address field
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_address',
            'placeholder': 'Start typing your address...'
        }),
        label='Street Address (Optional)'
    )
    
    class Meta:
        model = Vehicle
        fields = [
            'title', 'company', 'model', 'year', 'category', 'fuel_type',
            'transmission', 'mileage', 'condition', 'original_price', 'price',
            'description', 'features', 'address', 'city', 'seller_phone', 
            'image1', 'image2', 'image3', 'image4'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2020 Toyota Camry - Excellent Condition'
            }),
            'company': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_company'
            }),
            'model': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_model'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2020',
                'id': 'id_year'
            }),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'id_category'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_fuel_type'}),
            'transmission': forms.Select(attrs={'class': 'form-select', 'id': 'id_transmission'}),
            'mileage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50000',
                'id': 'id_mileage'
            }),
            'condition': forms.Select(attrs={'class': 'form-select', 'id': 'id_condition'}),
            'original_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30000',
                'id': 'id_original_price',
                'step': '0.01'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '25000',
                'id': 'id_price',
                'step': '0.01',
                'readonly': False
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your vehicle...'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'One feature per line\nLeather seats\nSunroof\nBackup camera'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dublin',
                'id': 'id_city'
            }),
            'seller_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0831234567'
            }),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
            'image4': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_year(self):
        """Validate year using custom library"""
        year = self.cleaned_data.get('year')
        is_valid, message = VehicleValidator.validate_year(year)
        if not is_valid:
            raise forms.ValidationError(message)
        return year
    
    def clean_price(self):
        """Validate price using custom library"""
        price = self.cleaned_data.get('price')
        is_valid, message = VehicleValidator.validate_price(price)
        if not is_valid:
            raise forms.ValidationError(message)
        return price
    
    def clean_mileage(self):
        """Validate mileage using custom library"""
        mileage = self.cleaned_data.get('mileage')
        is_valid, message = VehicleValidator.validate_mileage(mileage)
        if not is_valid:
            raise forms.ValidationError(message)
        return mileage
    
    def clean_seller_phone(self):
        """Validate phone using custom library"""
        phone = self.cleaned_data.get('seller_phone')
        is_valid, message = VehicleValidator.validate_phone(phone)
        if not is_valid:
            raise forms.ValidationError(message)
        return phone


class SearchForm(forms.Form):
    """Search and filter form"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title...'
        })
    )
    
    company = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'search_company',
            'placeholder': 'Select Company...'
        })
    )
    
    model = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'search_model',
            'placeholder': 'Select Model...'
        })
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Vehicle.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )
    
    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )


class OrderForm(forms.ModelForm):
    """Form for placing online orders - CASH ON DELIVERY ONLY"""
    
    # Buyer Information Fields
    buyer_full_name = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'John Doe'
        }),
        label='Full Name'
    )
    
    buyer_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        label='Email Address'
    )
    
    buyer_phone = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0831234567'
        }),
        label='Phone Number'
    )
    
    class Meta:
        model = Order
        fields = [
            'buyer_full_name', 'buyer_email', 'buyer_phone',
            'delivery_address', 'delivery_city', 'delivery_postal_code',
            'notes'
        ]
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Street address, apartment, suite, etc.',
                'id': 'id_delivery_address'
            }),
            'delivery_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'id': 'id_delivery_city'
            }),
            'delivery_postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code',
                'id': 'id_delivery_postal_code'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any additional notes for the seller'
            }),
        }