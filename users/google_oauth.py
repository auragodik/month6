import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.serializers import OAuthCodeSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import os

User = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Invalid access token!", "data": token_data}, status=400)

        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        email = user_info["email"]
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
                "registration_source": "google",
                "last_login": timezone.now()
            }
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True
            user.registration_source = "google"
            user.last_login = timezone.now()
            user.save(update_fields=["first_name", "last_name", "is_active", "registration_source", "last_login"])

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })
