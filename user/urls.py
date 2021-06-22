from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import RegistrationAPIView, LoginAPIView
from user import views
from rest_framework import routers

app_name = 'user'

router = routers.DefaultRouter()
router.register("api/user", views.UserViewSet)
router.register("api/role", views.RoleViewSet)
# router.register("api/user/reg", views.RegistrationAPIView)
# router.register("api/user/log", views.LoginAPIView)


urlpatterns = [
    path('api/user/reg', RegistrationAPIView.as_view()),
    path('api/user/log', LoginAPIView.as_view()),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls