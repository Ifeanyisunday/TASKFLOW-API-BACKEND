from django.test import TestCase

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser

@pytest.mark.django_db
class TestAuth:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_register_user(self, client):
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "strongpassword123"
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert CustomUser.objects.filter(email="test@example.com").exists()

    def test_login_user(self, client):
        # First create user
        user = CustomUser.objects.create_user(
            email="login@example.com",
            username="loginuser",
            password="password123"
        )

        url = reverse("login")
        data = {
            "email": "login@example.com",
            "password": "password123"
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]

    def test_logout_user_requires_auth(self, client):
        url = reverse("logout")
        response = client.post(url, {}, format="json")
        assert response.status_code == 401  # Unauthorized if not logged in