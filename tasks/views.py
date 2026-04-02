from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import TaskSerializer
from users.permissions import IsOwner
from django.utils import timezone


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # ✅ Combine ALL filters
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # ✅ Existing filters
    filterset_fields = ["status", "priority"]

    # ✅ Search
    search_fields = ["title", "description"]

    # ✅ Ordering
    ordering_fields = ["due_date", "priority", "created_at"]
    ordering = ["-created_at"]  # default ordering

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    # Assign the logged-in user automatically on create
    def perform_create(self, serializer):
        serializer.save()