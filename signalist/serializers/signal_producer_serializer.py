from rest_framework import serializers

from signal_producer.constants.base_constants import BaseConstants
from signal_producer.constants.channel_addresses_constants import channel_addresses_constants


class SignalProducerSerializer(serializers.Serializer):
    currency_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    desired_price = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    return_channel_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    @staticmethod
    def validate_return_channel_name(value):
        if value not in channel_addresses_constants.keys():
            raise serializers.ValidationError("Channel name is not a valid choice.")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)

        representation[BaseConstants.currency_name] = representation.get(BaseConstants.currency_name).replace('/', '')

        return representation

    class Meta:
        fields = [
            BaseConstants.currency_name,
            BaseConstants.desired_price,
            BaseConstants.return_channel_name,
        ]
