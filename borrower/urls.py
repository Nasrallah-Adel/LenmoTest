from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from borrower.views import LoanRequest

app_name = 'borrower'
# schema_view = get_swagger_view(title='borrower')
urlpatterns = [
    path('loan_request/', LoanRequest.as_view()),

]
