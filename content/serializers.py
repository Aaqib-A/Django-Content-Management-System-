import json

from rest_framework import serializers
from content.models import Content

class ContentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
        # fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["categories"] = representation["categories"].split(",")
        return representation