from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        due_date = validated_data.get("due_date")
        if due_date and timezone.is_naive(due_date):
            validated_data["due_date"] = timezone.make_aware(due_date)

        return Task.objects.create(
            user=self.context["request"].user,
            **validated_data
        )