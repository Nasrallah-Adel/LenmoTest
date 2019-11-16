from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


from investor.views import *

app_name = 'investor'
schema_view = get_swagger_view(title='investor')
urlpatterns = [
    path('creat_offer/', OfferCreate.as_view()),
    path('deposit_money/', DepositMoney.as_view()),
    path('loans/', LoanList.as_view()),
    path('offers/', OfferList.as_view()),


]
