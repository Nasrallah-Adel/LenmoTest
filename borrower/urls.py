from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


from borrower.views import *


app_name = 'borrower'
# schema_view = get_swagger_view(title='borrower')
urlpatterns = [
    path('loan_request/', LoanRequestCreate.as_view()),
    path('my_loans/', LoanRequestList.as_view()),
    path('accept_offer/', AcceptOffer.as_view()),
    path('deposit_money/', DepositMoney.as_view()),

]
