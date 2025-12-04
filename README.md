# Vehicle Marketplace Utils

A comprehensive Python library for vehicle marketplace applications, providing utilities for validation, price estimation, and data formatting.

**Student ID:** x23311428  
**Author:** Dhruv Jani

## Installation
```bash
pip install vehicle-market-x23311428
```

## Features

- **VehicleValidator**: Validate year, price, mileage, and phone numbers
- **PriceEstimator**: Calculate vehicle depreciation and estimate resale prices
- **VehicleFormatter**: Format prices, mileage, age, and phone numbers for display

## Quick Start

### Validation
```python
from vehicle_utils import VehicleValidator

# Validate year
is_valid, message = VehicleValidator.validate_year(2020)
print(f"Valid: {is_valid}, Message: {message}")

# Validate price
is_valid, message = VehicleValidator.validate_price(25000)

# Validate mileage
is_valid, message = VehicleValidator.validate_mileage(50000)

# Validate phone
is_valid, message = VehicleValidator.validate_phone("1234567890")
```

### Price Estimation
```python
from vehicle_utils import PriceEstimator

# Estimate vehicle price
result = PriceEstimator.estimate_price(
    original_price=30000,
    year_of_purchase=2018,
    category='sedan',
    fuel_type='petrol',
    transmission='automatic',
    mileage=50000,
    condition='good'
)

print(f"Estimated Price: €{result['estimated_price']}")
print(f"Depreciation: {result['total_depreciation_percentage']}%")
print(f"Vehicle Age: {result['age']} years")
```

### Data Formatting
```python
from vehicle_utils import VehicleFormatter

# Format price
formatted_price = VehicleFormatter.format_price(25000)
print(formatted_price)  # €25,000

# Format mileage
formatted_mileage = VehicleFormatter.format_mileage(50000)
print(formatted_mileage)  # 50,000 km

# Format age
age = VehicleFormatter.format_age(2020)
print(age)  # 5 years old

# Format phone
phone = VehicleFormatter.format_phone("1234567890")
print(phone)  # 123-456-7890
```

## Depreciation Model

The price estimator uses a sophisticated depreciation model:

- **Year 1**: 20% depreciation
- **Years 2-5**: 15% depreciation per year
- **Year 6+**: 10% depreciation per year

### Additional Factors

- **Category**: SUVs (+15%), Trucks (+10%), Coupes (-10%)
- **Fuel Type**: Electric (+20%), Hybrid (+10%), Diesel (+5%)
- **Transmission**: Automatic (+5%), Manual (-5%)
- **Mileage**: 2% depreciation per 10,000 km
- **Condition**: Excellent (+10%), Good (baseline), Fair (-15%), Poor (-30%)

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT License