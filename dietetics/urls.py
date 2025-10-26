from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'personal-databases', views.PersonnalDatabasesViewSet)
router.register(r'foods', views.FoodsViewSet)
router.register(r'comments', views.CommentsViewSet)
router.register(r'imc-histories', views.ImcHistoriesViewSet)
router.register(r'dej-histories', views.DejHistoriesViewSet)
router.register(r'undernutrition-adult-histories', views.UndernutritionAdultHistoriesViewSet)
router.register(r'undernutrition-senior-histories', views.UndernutritionSeniorHistoriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/login/', views.CustomLoginView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
]