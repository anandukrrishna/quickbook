from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event

        fields = '__all__'

        read_only_fields = [
            'id',
            'available_seats',
            'created_at',
            'updated_at',
        ]

    def validate_total_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Total seats must be greater than zero."
            )

        return value

    def create(self, validated_data):
        validated_data['available_seats'] = (
            validated_data['total_seats']
        )

        return super().create(validated_data)