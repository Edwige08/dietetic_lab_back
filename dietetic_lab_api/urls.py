from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_home(request):
    return JsonResponse({
        "message": "Dietetic Lab API",
        "status": "running",
        "version": "1.0",
    })

urlpatterns = [
    path('', api_home, name='api_home'),  # Route pour la racine
    path('admin/', admin.site.urls),
    path('api/v1/', include('dietetics.urls')),
]