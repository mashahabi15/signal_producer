from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from signal_producer.constants.base_constants import BaseConstants
from signal_producer.utils.response_utils import ResponseUtils
from signalist import tasks
from signalist.serializers.signal_producer_serializer import SignalProducerSerializer


class CurrencyPairSignalistView(GenericAPIView):
    http_method_names = [
        BaseConstants.get_method_str,
    ]

    serializer_class = SignalProducerSerializer

    def __init__(self):
        super().__init__()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=False):
            data = serializer.data
            tasks.producer_task(currency_name=data.get(BaseConstants.currency_name))
            tasks.signaler_task(
                currency_name=data.get(BaseConstants.currency_name),
                return_channel_name=data.get(BaseConstants.return_channel_name),
                desired_price=data.get(BaseConstants.desired_price))

        result = ResponseUtils.get_final_response_result(
            code=status.HTTP_400_BAD_REQUEST,
            status=BaseConstants.error,
            data=serializer.errors)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=result)
