from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def api_home(request):
    return JsonResponse({
        "message": "Dietetic Lab API",
        "status": "running",
        "version": "1.0",
        "documentation": "api/docs",
    })

urlpatterns = [
    path('', api_home, name='api_home'),  # Route pour la racine
    path('admin/', admin.site.urls),
    path('api/v1/', include('dietetics.urls')),
    
    # Swagger/OpenAPI documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]