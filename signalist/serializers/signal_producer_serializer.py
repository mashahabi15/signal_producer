from rest_framework import serializers


class CurrencyPairSignalistSerializer(serializers.Serializer):
    currency_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    return_channel_address = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    return_channel_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        fields = [
            'currency_name',
            'return_channel_address',
            'return_channel_name',
        ]
