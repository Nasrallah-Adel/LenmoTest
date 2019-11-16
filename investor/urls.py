from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from investor.views import *

app_name = 'investor'
schema_view = get_swagger_view(title='investor')
urlpatterns = [
    path('creat_offer/', OfferCreate.as_view()),

]
