from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vehicle, Favorite, Order
from .forms import VehicleForm, SearchForm, OrderForm
from vehicle_utils import PriceEstimator
from django.http import JsonResponse


def calculate_price_api(request):
    """API endpoint to calculate estimated price"""
    if request.method == 'GET':
        try:
            # Get parameters from GET request
            original_price = float(request.GET.get('original_price', 0))
            year = int(request.GET.get('year', 2020))
            category = request.GET.get('category', 'sedan')
            fuel_type = request.GET.get('fuel_type', 'petrol')
            transmission = request.GET.get('transmission', 'manual')
            mileage = int(request.GET.get('mileage', 0))
            condition = request.GET.get('condition', 'good')
            
            # Calculate estimate
            estimation = PriceEstimator.estimate_price(
                original_price=original_price,
                year_of_purchase=year,
                category=category,
                fuel_type=fuel_type,
                transmission=transmission,
                mileage=mileage,
                condition=condition
            )
            
            return JsonResponse({
                'success': True,
                'estimated_price': estimation['estimated_price'],
                'details': estimation
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def home(request):
    """Homepage with featured and recent vehicles"""
    featured_vehicles = Vehicle.objects.filter(is_sold=False, is_featured=True)[:6]
    recent_vehicles = Vehicle.objects.filter(is_sold=False)[:8]
    
    context = {
        'featured': featured_vehicles,
        'recent': recent_vehicles,
    }
    return render(request, 'vehicles/home.html', context)


def vehicle_list(request):
    """List all vehicles with search and filters"""
    vehicles = Vehicle.objects.filter(is_sold=False).order_by('-created_at')
    
    # Apply search filters
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        company = form.cleaned_data.get('company')
        model = form.cleaned_data.get('model')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if query:
            vehicles = vehicles.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if company:
            vehicles = vehicles.filter(company__iexact=company)
        
        if model:
            vehicles = vehicles.filter(model__iexact=model)
        
        if category:
            vehicles = vehicles.filter(category=category)
        
        if min_price:
            vehicles = vehicles.filter(price__gte=min_price)
        
        if max_price:
            vehicles = vehicles.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(vehicles, 12)
    page_number = request.GET.get('page')
    vehicles = paginator.get_page(page_number)
    
    context = {
        'vehicles': vehicles,
        'form': form,
    }
    return render(request, 'vehicles/vehicle_list.html', context)


@login_required
def vehicle_detail(request, pk):
    """Display vehicle details - LOGIN REQUIRED"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Check if user has favorited this vehicle
    is_favorited = Favorite.objects.filter(user=request.user, vehicle=vehicle).exists()
    
    # Get similar vehicles (same company or category)
    similar_vehicles = Vehicle.objects.filter(
        Q(company=vehicle.company) | Q(category=vehicle.category)
    ).exclude(pk=vehicle.pk).filter(is_sold=False)[:4]
    
    # Check if user has already ordered
    has_order = Order.objects.filter(buyer=request.user, vehicle=vehicle).exists()
    
    context = {
        'vehicle': vehicle,
        'is_favorited': is_favorited,
        'similar_vehicles': similar_vehicles,
        'has_order': has_order,
        'is_owner': vehicle.seller == request.user,
    }
    return render(request, 'vehicles/vehicle_detail.html', context)


@login_required
def vehicle_create(request):
    """Create new vehicle listing - CREATE operation"""
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.seller = request.user
            vehicle.save()
            messages.success(request, 'Vehicle listing created successfully!')
            return redirect('vehicle_detail', pk=vehicle.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm()
    
    context = {
        'form': form,
        'title': 'Sell Your Car'
    }
    return render(request, 'vehicles/vehicle_form.html', context)


@login_required
def vehicle_update(request, pk):
    """Update existing vehicle - UPDATE operation"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Check if user owns this vehicle
    if vehicle.seller != request.user:
        messages.error(request, 'You can only edit your own listings.')
        return redirect('vehicle_detail', pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicle_detail', pk=vehicle.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm(instance=vehicle)
    
    context = {
        'form': form,
        'vehicle': vehicle,
        'title': 'Edit Listing'
    }
    return render(request, 'vehicles/vehicle_form.html', context)


@login_required
def vehicle_delete(request, pk):
    """Delete vehicle listing - DELETE operation"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Check if user owns this vehicle
    if vehicle.seller != request.user:
        messages.error(request, 'You can only delete your own listings.')
        return redirect('vehicle_detail', pk=pk)
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('home')
    
    context = {'vehicle': vehicle}
    return render(request, 'vehicles/vehicle_confirm_delete.html', context)


@login_required
def my_listings(request):
    """Display user's vehicle listings"""
    vehicles = Vehicle.objects.filter(seller=request.user).order_by('-created_at')
    
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'vehicles/my_listings.html', context)


def search(request):
    """Search vehicles"""
    vehicles = Vehicle.objects.filter(is_sold=False).order_by('-created_at')
    
    # Apply search filters
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        company = form.cleaned_data.get('company')
        model = form.cleaned_data.get('model')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if query:
            vehicles = vehicles.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if company:
            vehicles = vehicles.filter(company__iexact=company)
        
        if model:
            vehicles = vehicles.filter(model__iexact=model)
        
        if category:
            vehicles = vehicles.filter(category=category)
        
        if min_price:
            vehicles = vehicles.filter(price__gte=min_price)
        
        if max_price:
            vehicles = vehicles.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(vehicles, 12)
    page_number = request.GET.get('page')
    vehicles = paginator.get_page(page_number)
    
    context = {
        'vehicles': vehicles,
        'form': form,
        'query': request.GET.get('query', ''),
    }
    return render(request, 'vehicles/vehicle_list.html', context)


@login_required
def toggle_favorite(request, pk):
    """Add or remove vehicle from favorites"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        vehicle=vehicle
    )
    
    if not created:
        # Already favorited, so remove it
        favorite.delete()
        messages.success(request, 'Removed from favorites.')
    else:
        messages.success(request, 'Added to favorites!')
    
    return redirect('vehicle_detail', pk=pk)


@login_required
def my_favorites(request):
    """Display user's favorite vehicles"""
    favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')
    
    context = {
        'favorites': favorites,
    }
    return render(request, 'vehicles/my_favorites.html', context)


@login_required
def place_order(request, pk):
    """Place an order for online purchase"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Check if vehicle is already sold
    if vehicle.is_sold:
        messages.error(request, "Sorry, this vehicle has already been sold!")
        return redirect('vehicle_detail', pk=pk)
    
    # Don't allow seller to buy their own vehicle
    if vehicle.seller == request.user:
        messages.error(request, "You cannot buy your own vehicle!")
        return redirect('vehicle_detail', pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.vehicle = vehicle
            order.buyer = request.user
            order.total_amount = vehicle.price
            
            # Save card details if card payment
            if order.payment_method == 'card':
                order.card_number = form.cleaned_data.get('card_number', '')
                order.card_name = form.cleaned_data.get('card_name', '')
                order.card_expiry = form.cleaned_data.get('card_expiry', '')
                order.status = 'paid'
            else:
                order.status = 'pending'
            
            order.save()
            
            messages.success(
                request, 
                f'Order placed successfully! Order ID: #{order.id}'
            )
            
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    
    context = {
        'vehicle': vehicle,
        'form': form,
    }
    return render(request, 'vehicles/place_order.html', context)


@login_required
def order_confirmation(request, order_id):
    """Display order confirmation"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    context = {'order': order}
    return render(request, 'vehicles/order_confirmation.html', context)


@login_required
def my_orders(request):
    """View user's purchase orders"""
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'vehicles/my_orders.html', context)


@login_required
def seller_orders(request):
    """View orders for seller's vehicles"""
    # Get all orders for vehicles sold by this user
    orders = Order.objects.filter(vehicle__seller=request.user).order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'vehicles/seller_orders.html', context)


@login_required
def confirm_order(request, order_id):
    """Confirm an order as seller"""
    order = get_object_or_404(Order, id=order_id, vehicle__seller=request.user)
    
    if request.method == 'POST':
        order.seller_confirmed = True
        order.status = 'confirmed'
        order.save()
        
        # Mark the vehicle as sold
        vehicle = order.vehicle
        vehicle.is_sold = True
        vehicle.save()
        
        messages.success(
            request, 
            f'Order #{order.id} confirmed successfully! Vehicle marked as SOLD.'
        )
        return redirect('seller_orders')
    
    return redirect('seller_orders')


@login_required
def reject_order(request, order_id):
    """Reject an order as seller"""
    order = get_object_or_404(Order, id=order_id, vehicle__seller=request.user)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        
        messages.success(
            request, 
            f'Order #{order.id} has been rejected.'
        )
        return redirect('seller_orders')
    
    return redirect('seller_orders')