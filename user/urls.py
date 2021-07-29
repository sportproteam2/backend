from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user import views
from rest_framework import routers

app_name = 'user'

router = routers.DefaultRouter()
# router.register("api/user", views.UserViewSet)
router.register("api/role", views.RoleViewSet)
router.register("api/region", views.RegionView)
router.register("api/trainers", views.TrainerView)
# router.register("api/user/reg", views.RegistrationAPIView)
# router.register("api/user/log", views.LoginAPIView)



urlpatterns = [
    path('api/user/', views.UsersAPIView.as_view()),
    path('api/user/<int:pk>', views.UsersDetail.as_view()),
    path('api/user/reg/', views.RegistrationAPIView.as_view()),
    path('api/user/log', views.LoginAPIView.as_view()),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls