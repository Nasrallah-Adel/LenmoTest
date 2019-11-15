from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from pip._vendor.html5lib.treeadapters.sax import namespace
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

from LenmoTest.veiw import Login, Register

app_name = 'apis'
schema_view = get_swagger_view(title='apis')
urlpatterns = [
                  path('api-token/', obtain_jwt_token),
                  path('login/', Login.as_view()),
                  path('register/', Register.as_view()),

                  path('borrower/', include('borrower.urls', namespace='borrower')),
                  path('investor/', include('investor.urls', namespace='investor')),
                  path('', schema_view),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
