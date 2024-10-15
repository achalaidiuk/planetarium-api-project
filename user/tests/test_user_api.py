from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserURLsTest(APITestCase):

    def test_register_url(self):
        url = reverse("user:create")
        data = {"username": "newuser", "password": "newpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_url(self):
        url = reverse("user:token_obtain_pair")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_token_refresh_url(self):
        url = reverse("user:token_refresh")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_token_verify_url(self):
        url = reverse("user:token_verify")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_manage_user_url(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        url = reverse("user:manage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_obtain_jwt_token(self):
        url = reverse("user:token_obtain_pair")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_refresh_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse("user:token_refresh")
        data = {"refresh": str(refresh)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_verify_jwt_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        url = reverse("user:token_verify")
        data = {"token": access_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_user_unauthenticated(self):
        url = reverse("user:manage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
