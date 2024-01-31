from rest_framework import serializers

class UserVerificationMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()