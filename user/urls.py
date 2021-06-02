from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UsersAPIView, RoleAPIView, RoleDetail, UsersDetail, RegistrationAPIView, LoginAPIView

app_name = 'user'
urlpatterns = [
    path('api/user/reg', RegistrationAPIView.as_view()),
    path('api/user/log', LoginAPIView.as_view()),
    path('api/user', UsersAPIView.as_view()),
    path('api/user/<int:pk>', UsersDetail.as_view()),
    path('api/role', RoleAPIView.as_view()),
    path('api/role/<int:pk>', RoleDetail.as_view()),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]