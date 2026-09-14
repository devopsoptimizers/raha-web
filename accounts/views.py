from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, RoleAccess
from .serializers import ChangePasswordSerializer, EmailSerializer, LoginSerializer, LogoutSerializer, ResetPasswordSerializer, UserSerializer, UserAdminSerializer, RoleAccessSerializer

class IsSuperAdministrator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (request.user.is_superuser or request.user.role == User.Role.SUPER_ADMIN))

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserAdminSerializer
    permission_classes = (IsSuperAdministrator,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("email", "username", "first_name", "last_name", "phone")
    ordering_fields = ("date_joined", "email", "role", "is_active")

class RoleAccessViewSet(viewsets.ModelViewSet):
    queryset = RoleAccess.objects.all().order_by("role")
    serializer_class = RoleAccessSerializer
    permission_classes = (IsSuperAdministrator,)
    http_method_names = ("get", "patch", "head", "options")

class MyPermissionsView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.is_superuser or request.user.role == User.Role.SUPER_ADMIN:
            return Response({"permissions": ["all"]})
        policy = RoleAccess.objects.filter(role=request.user.role).first()
        return Response({"permissions": policy.permissions if policy else []})

class LoginThrottle(AnonRateThrottle):
    scope = "login"

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return Response({"refresh": ["This field is required."]}, status=400)
        RefreshToken(token).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self): return self.request.user

class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Incorrect password."]}, status=400)
        request.user.set_password(serializer.validated_data["new_password"]); request.user.save(update_fields=["password"])
        update_session_auth_hash(request, request.user)
        return Response({"detail": "Password changed."})

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]; serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data["email"], is_active=True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk)); token = default_token_generator.make_token(user)
            send_mail("Password reset", f"Reset token: {uid}/{token}", None, [user.email])
        return Response({"detail": "If the account exists, reset instructions were sent."})

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]; serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        try: user = User.objects.get(pk=force_str(urlsafe_base64_decode(serializer.validated_data["uid"])))
        except (User.DoesNotExist, ValueError, TypeError): return Response({"token": ["Invalid token."]}, status=400)
        if not default_token_generator.check_token(user, serializer.validated_data["token"]): return Response({"token": ["Invalid token."]}, status=400)
        password_validation.validate_password(serializer.validated_data["new_password"], user)
        user.set_password(serializer.validated_data["new_password"]); user.save(update_fields=["password"])
        return Response({"detail": "Password reset successful."})
