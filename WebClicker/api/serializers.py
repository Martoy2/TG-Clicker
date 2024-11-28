from main.models import TelegramUser, Pool, History
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'

    def create(self, validated_data):
        return TelegramUser.objects.create(**validated_data)


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['user_id', 'action', 'ticket_count', 'coin_count', 'balance']

    def create(self, validated_data):
        return History.objects.create(**validated_data)
