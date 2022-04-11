import json
from datetime import datetime

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from signal_producer.adapters.redis_adapter import RedisAdapter
from signal_producer.constants.base_constants import BaseConstants
from signal_producer.utils.response_utils import ResponseUtils
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
            self._create_producer_task(data)
            self._create_signaler_task(data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        result = ResponseUtils.get_final_response_result(
            code=status.HTTP_400_BAD_REQUEST,
            status=BaseConstants.error,
            data=serializer.errors)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=result)

    @staticmethod
    def _create_producer_task(data):
        if not RedisAdapter().get_currency_pair_list_redis_cache() or \
                data.get(BaseConstants.currency_name) not in RedisAdapter().get_currency_pair_list_redis_cache():
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.MINUTES)

            PeriodicTask.objects.create(
                interval=schedule,
                name='Producing Signals {}'.format(datetime.now()),
                task='signalist.tasks.producer_task',
                kwargs=json.dumps({
                    BaseConstants.currency_name: data.get(BaseConstants.currency_name)})
            )

            RedisAdapter().set_currency_pair_list_redis_cache(new_currency_name=data.get(BaseConstants.currency_name))

    @staticmethod
    def _create_signaler_task(data):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES)

        PeriodicTask.objects.create(
            interval=schedule,
            name='Sending Signals {}'.format(datetime.now()),
            task='signalist.tasks.signaler_task',
            kwargs=json.dumps({
                BaseConstants.currency_name: data.get(BaseConstants.currency_name),
                BaseConstants.return_channel_name: data.get(BaseConstants.return_channel_name),
                BaseConstants.desired_price: data.get(BaseConstants.desired_price),
            })
        )
