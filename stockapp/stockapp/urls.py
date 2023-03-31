from django.contrib import admin
from django.urls import path, include
from api import views
from users.views import EmailRegistration, GoogleCallbackHandler
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userinfo/', views.user_detail),
    path('current_user/', views.current_user),
    path('create_user/', views.create_user),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', EmailRegistration.as_view()),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('api/google/callback/', GoogleCallbackHandler.as_view(), name='google-callback'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('add-stock/', views.add_stock),
    path('get-stock/<int:id>/', views.get_stock),
    path('buy-stock/', views.buy_stock),
    path('sell-stock/', views.sell_stock),
    path('get-users-stock/', views.get_users_stock),
    path('get-transactions/', views.get_users_transaction),
    path('add-watchlist/', views.add_in_watchlist),
    path('remove-watchlist/', views.remove_from_watchlist),
    path('get-watchlist/', views.get_watchlist),
]
