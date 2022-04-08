from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from currency_pair_signalist.constants.base_constants import BaseConstants
from currency_pair_signalist.utils.response_utils import ResponseUtils
from signalist.serializers.currency_pair_signalist_serializer import CurrencyPairSignalistSerializer


class CurrencyPairSignalistView(GenericAPIView):
    http_method_names = [
        BaseConstants.get_method_str,
    ]

    serializer_class = CurrencyPairSignalistSerializer

    def __init__(self):
        super().__init__()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        if serializer.is_valid(raise_exception=False):
            pass

        result = ResponseUtils.get_final_response_result(
            code=status.HTTP_400_BAD_REQUEST,
            status=BaseConstants.error,
            data=serializer.errors)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=result)
