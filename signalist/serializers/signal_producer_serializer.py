from rest_framework import serializers


class CurrencyPairSignalistSerializer(serializers.Serializer):
    currency_pair_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    return_channel_address = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    return_channel_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        fields = [
            'currency_pair_name',
            'return_channel_address',
            'return_channel_name',
        ]
