from rest_framework import serializers


class InitDataSerializer(serializers.Serializer):
    init_data = serializers.CharField()
