from django.urls import path
from rest_framework.routers import DefaultRouter

from signalist.views.signal_producer_view import CurrencyPairSignalistView

app_name = "signalist"

router = DefaultRouter()

urlpatterns = [

    path('currency_pair/', CurrencyPairSignalistView.as_view(), name='signal_producer_view'),

]

urlpatterns += router.urls
