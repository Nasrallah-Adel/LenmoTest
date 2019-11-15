from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
app_name = 'investor'
schema_view = get_swagger_view(title='investor')
urlpatterns = [
    # path('register/', Register.as_view()),

]
