import re
from datetime import datetime

__version__ = '1.0.0'


class VehicleValidator:
    """Validates vehicle data inputs"""
    
    @staticmethod
    def validate_year(year):
        """Validate manufacturing year"""
        try:
            year = int(year)
            current_year = datetime.now().year
            if year < 1900 or year > current_year + 1:
                return False, "Invalid year"
            return True, "Valid"
        except:
            return False, "Year must be a number"
    
    @staticmethod
    def validate_price(price):
        """Validate price"""
        try:
            price = float(price)
            if price <= 0:
                return False, "Price must be positive"
            if price > 10000000:
                return False, "Price too high"
            return True, "Valid"
        except:
            return False, "Invalid price"
    
    @staticmethod
    def validate_mileage(mileage):
        """Validate mileage in kilometers"""
        try:
            mileage = int(mileage)
            if mileage < 0:
                return False, "Mileage cannot be negative"
            if mileage > 1000000:
                return False, "Mileage unrealistic"
            return True, "Valid"
        except:
            return False, "Invalid mileage"
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        phone = re.sub(r'\D', '', str(phone))
        if len(phone) < 10 or len(phone) > 15:
            return False, "Phone must be 10-15 digits"
        return True, "Valid"


class VehicleFormatter:
    """Formats vehicle data for display"""
    
    @staticmethod
    def format_price(price, currency='€'):
        """Format price with currency symbol"""
        try:
            price_float = float(price)
            return f"{currency}{price_float:,.0f}"
        except:
            return f"{currency}0"
    
    @staticmethod
    def format_mileage(mileage):
        """Format mileage with km"""
        try:
            mileage_int = int(mileage)
            return f"{mileage_int:,} km"
        except:
            return "0 km"
    
    @staticmethod
    def format_age(year):
        """Calculate and format vehicle age"""
        try:
            year_int = int(year)
            age = datetime.now().year - year_int
            if age == 0:
                return "Brand New"
            elif age == 1:
                return "1 year old"
            else:
                return f"{age} years old"
        except:
            return "Unknown age"
    
    @staticmethod
    def format_phone(phone):
        """Format phone number"""
        phone_digits = re.sub(r'\D', '', str(phone))
        if len(phone_digits) == 10:
            return f"{phone_digits[:3]}-{phone_digits[3:6]}-{phone_digits[6:]}"
        return phone


class PriceEstimator:
    """Estimates vehicle resale price based on various factors"""
    
    # Depreciation rates per year
    DEPRECIATION_RATES = {
        'year_1': 0.20,      # 20% in first year
        'year_2_5': 0.15,    # 15% per year for years 2-5
        'year_6_plus': 0.10  # 10% per year after year 5
    }
    
    # Category multipliers
    CATEGORY_MULTIPLIERS = {
        'sedan': 1.0,
        'suv': 1.15,     
        'hatchback': 0.95,
        'truck': 1.10,
        'coupe': 0.90,
        'van': 0.95,
    }
    
    # Fuel type multipliers
    FUEL_MULTIPLIERS = {
        'petrol': 1.0,
        'diesel': 1.05,
        'electric': 1.20,   
        'hybrid': 1.10,
    }
    
    # Transmission multipliers
    TRANSMISSION_MULTIPLIERS = {
        'manual': 0.95,
        'automatic': 1.05, 
    }
    
    # Condition multipliers
    CONDITION_MULTIPLIERS = {
        'excellent': 1.10,
        'good': 1.0,
        'fair': 0.85,
        'poor': 0.70,
    }
    
    # Mileage impact (per 10,000 km)
    MILEAGE_DEPRECIATION = 0.02  # 2% per 10,000 km
    
    @classmethod
    def calculate_depreciation(cls, original_price, year_of_purchase):
        """
        Calculate depreciation based on age
        
        Args:
            original_price: Original purchase price
            year_of_purchase: Year when car was purchased
            
        Returns:
            dict: Depreciation details including age, depreciated value, and percentages
        """
        current_year = datetime.now().year
        age = current_year - year_of_purchase
        
        if age < 0:
            age = 0
        
        depreciated_value = float(original_price)
        
        # First year depreciation
        if age >= 1:
            depreciated_value *= (1 - cls.DEPRECIATION_RATES['year_1'])
            remaining_years = age - 1
        else:
            remaining_years = 0
        
        # Years 2-5 depreciation
        years_2_5 = min(remaining_years, 4)
        if years_2_5 > 0:
            for _ in range(years_2_5):
                depreciated_value *= (1 - cls.DEPRECIATION_RATES['year_2_5'])
            remaining_years -= years_2_5
        
        # Years 6+ depreciation
        if remaining_years > 0:
            for _ in range(remaining_years):
                depreciated_value *= (1 - cls.DEPRECIATION_RATES['year_6_plus'])
        
        return {
            'age': age,
            'depreciated_value': round(depreciated_value, 2),
            'total_depreciation': round(float(original_price) - depreciated_value, 2),
            'depreciation_percentage': round(((float(original_price) - depreciated_value) / float(original_price)) * 100, 2)
        }
    
    @classmethod
    def estimate_price(cls, original_price, year_of_purchase, category, fuel_type, 
                      transmission, mileage, condition):
        """
        Estimate current market price of vehicle
        
        Args:
            original_price: Original purchase price
            year_of_purchase: Year when car was purchased
            category: Vehicle category (sedan, suv, etc.)
            fuel_type: Fuel type (petrol, diesel, etc.)
            transmission: Transmission type (manual, automatic)
            mileage: Current mileage in kilometers
            condition: Current condition (excellent, good, fair, poor)
            
        Returns:
            dict: Estimated price with breakdown of all factors
        """
        # Start with depreciation
        depreciation_info = cls.calculate_depreciation(original_price, year_of_purchase)
        base_value = depreciation_info['depreciated_value']
        
        # Apply category multiplier
        category_factor = cls.CATEGORY_MULTIPLIERS.get(category, 1.0)
        
        # Apply fuel type multiplier
        fuel_factor = cls.FUEL_MULTIPLIERS.get(fuel_type, 1.0)
        
        # Apply transmission multiplier
        transmission_factor = cls.TRANSMISSION_MULTIPLIERS.get(transmission, 1.0)
        
        # Apply condition multiplier
        condition_factor = cls.CONDITION_MULTIPLIERS.get(condition, 1.0)
        
        # Calculate mileage impact
        mileage_units = mileage / 10000  
        mileage_factor = 1 - (mileage_units * cls.MILEAGE_DEPRECIATION)
        mileage_factor = max(mileage_factor, 0.5)  
        
        # Calculate final estimated price
        estimated_price = base_value * category_factor * fuel_factor * transmission_factor * condition_factor * mileage_factor
        estimated_price = round(estimated_price, 2)
        
        return {
            'estimated_price': estimated_price,
            'original_price': float(original_price),
            'age': depreciation_info['age'],
            'base_depreciated_value': base_value,
            'category_impact': round((category_factor - 1) * 100, 2),
            'fuel_impact': round((fuel_factor - 1) * 100, 2),
            'transmission_impact': round((transmission_factor - 1) * 100, 2),
            'condition_impact': round((condition_factor - 1) * 100, 2),
            'mileage_impact': round((mileage_factor - 1) * 100, 2),
            'total_depreciation_percentage': round(((float(original_price) - estimated_price) / float(original_price)) * 100, 2)
        }
    
    @classmethod
    def get_price_range(cls, estimated_price):
        """
        Get suggested price range for listing
        
        Args:
            estimated_price: Estimated market price
            
        Returns:
            dict: Price range with min, estimated, and max values
        """
        min_price = estimated_price * 0.90 
        max_price = estimated_price * 1.10 
        
        return {
            'min_price': round(min_price, 2),
            'estimated_price': estimated_price,
            'max_price': round(max_price, 2)
        }