from django.urls import path
from rest_framework.routers import DefaultRouter

from signalist.views.currency_pair_signalist_view import CurrencyPairSignalistView

app_name = "signalist"

router = DefaultRouter()

urlpatterns = [

    path('currency_pair/', CurrencyPairSignalistView.as_view(), name='currency_pair_signalist_view'),

]

urlpatterns += router.urls
