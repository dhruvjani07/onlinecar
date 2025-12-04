from django.conf import settings

def google_maps_key(request):
    """Make Google Maps API key available in all templates"""
    return {
        'settings': settings
    }