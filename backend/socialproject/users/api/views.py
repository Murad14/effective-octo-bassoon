from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, PasswordChangeSerializer, EmailSerializer, ResetPasswordSerializer
from rest_framework import status, serializers, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):

    def post(self, request, format=None):
        
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response({"message": "User successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token or token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        
class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            confirm_password = serializer.validated_data.get("confirm_password")
            
            user = self.request.user
            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_password != confirm_password:
                return Response({"detail": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(generics.GenericAPIView):
    
    serializer_class = EmailSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            reset_url = reverse(
                "password_reset_request",
                kwargs= {"encoded_pk": encoded_pk, "token": token},
            )
            
            reset_url = f"http://127.0.0.1:8000{reset_url}"
            
            # Send the password reset email
            subject = "Password Reset Request"
            message = f"Please click the following link to reset your password: {reset_url}"
            from_email = "EMAIL_HOST_USER" #sender email
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return Response(
                {
                    "detail": "Password reset email sent successfully.",
                    "message": f"reset link: {reset_url}"
                }, status=status.HTTP_200_OK)
        
        return Response({
            "detail": serializer.errors,
            "message": "User doesn't exists"
        },status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(generics.GenericAPIView):
    
    serializer_class = ResetPasswordSerializer
    
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"kwargs":kwargs}
        )
        serializer.is_valid(raise_exception=True)
        
        # Retrieve the user based on the encoded_pk
        encoded_pk = kwargs.get("encoded_pk")
        try:
            user = User.objects.get(pk=urlsafe_base64_decode(encoded_pk).decode())
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    
        serializer.save(user)
        
        return Response(
            {"message": "Password Reset Complete"},status=status.HTTP_200_OK
        )