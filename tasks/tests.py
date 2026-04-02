from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from tasks.models import Task
from users.models import CustomUser
from django.utils import timezone
from datetime import datetime

@pytest.mark.django_db
class TestTasks:
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="taskuser@example.com",
            username="taskuser",
            password="password123"
        )

    @pytest.fixture
    def client(self, user):
        client = APIClient()
        # login to get JWT
        response = client.post(
            reverse("login"),
            {"email": user.email, "password": "password123"},
            format="json"
        )
        token = response.data["tokens"]["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client

    def test_create_task(self, client):
        url = reverse("tasks-list")  # DRF router naming
        data = {
            "title": "Test Task",
            "description": "Unit test task",
            "priority": "high",
            "status": "todo",
            "due_date": "2026-04-05"
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert Task.objects.filter(title="Test Task").exists()

    def test_list_tasks_only_user_tasks(self, client, user):
        # create a task for another user
        other_user = CustomUser.objects.create_user(
            email="other@example.com",
            username="otheruser",
            password="password123"
        )
        Task.objects.create(
            title="Other Task",
            description="Other user's task",
            priority="low",
            status="todo",
            due_date=timezone.make_aware(datetime(2026, 4, 6)),
            user=other_user
        )

        # create a task for logged-in user
        Task.objects.create(
            title="My Task",
            description="My own task",
            priority="medium",
            status="todo",
            due_date=timezone.make_aware(datetime(2026, 4, 7)),
            user=user
        )

        url = reverse("tasks-list")
        response = client.get(url)
        assert response.status_code == 200

        data = response.json()
        # Should only return user's own task
        assert len(data['results']) == 1
        assert data['results'][0]['title'] == "My Task"

    def test_update_task(self, client, user):
        client.force_authenticate(user=user)

        task = Task.objects.create(
            title="Old Task",
            description="Update me",
            priority="low",
            status="todo",
            due_date= timezone.make_aware(datetime(2026, 4, 5)),
            user=user
        )

        url = reverse("tasks-detail", args=[task.id])
        response = client.patch(url, {"status": "in_progress"}, format="json")
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.status == "in_progress"

    def test_delete_task(self, client, user):
        task = Task.objects.create(
            title="Delete Me",
            description="Will be deleted",
            priority="low",
            status="todo",
            due_date=timezone.make_aware(datetime(2026, 4, 5)),
            user=user
        )
        url = reverse("tasks-detail", args=[task.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Task.objects.filter(id=task.id).exists()