from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # Vehicle CRUD operations
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # User features
    path('my-listings/', views.my_listings, name='my_listings'),
    path('search/', views.search, name='search'),
    path('vehicles/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    
    # Orders (Buyer)
    path('vehicles/<int:pk>/order/', views.place_order, name='place_order'),
    path('orders/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Orders (Seller)
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/orders/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
    path('seller/orders/<int:order_id>/reject/', views.reject_order, name='reject_order'),
    
    # API
    path('api/calculate-price/', views.calculate_price_api, name='calculate_price_api'),
]