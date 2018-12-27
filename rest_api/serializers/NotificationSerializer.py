from rest_framework import serializers


class VerifySerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)