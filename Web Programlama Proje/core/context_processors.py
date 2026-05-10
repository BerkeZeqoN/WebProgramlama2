"""
PULSE Platform — Core Context Processors
Provides global template context variables.
"""
from django.conf import settings


def platform_context(request):
    """Inject platform-wide variables into all templates."""
    return {
        'PLATFORM_NAME': 'PULSE',
        'PLATFORM_FULL_NAME': 'Platform for Unified Live Survey & Emergency Response',
        'PLATFORM_VERSION': '1.0.0',
        'DEBUG': settings.DEBUG,
    }
