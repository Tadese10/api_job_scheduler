from rest_framework import serializers


class DagSerializer(serializers.Serializer):
    dagId = serializers.CharField(max_length=50, required=True)

class CreateDagSerializer(serializers.Serializer):
    dagId = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(max_length=50, required=True)
    schedule_interval = serializers.DateField(required=True)


class DagPauseSerializer(serializers.Serializer):
    dagId = serializers.CharField(max_length=50, required=True)
    pause = serializers.BooleanField(default=True)