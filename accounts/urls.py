from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ChangePasswordView, ForgotPasswordView, LoginView, LogoutView, MeView, ResetPasswordView, UserAdminViewSet, RoleAccessViewSet, MyPermissionsView
router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="admin-user")
router.register("role-access", RoleAccessViewSet, basename="role-access")
urlpatterns = [
    path("login/", LoginView.as_view()), path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()), path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()), path("me/", MeView.as_view()),
    path("change-password/", ChangePasswordView.as_view()), path("my-permissions/", MyPermissionsView.as_view()),
] + [path("", include(router.urls))]
