import jwt
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, JSONWebTokenSerializer

from LenmoTest import settings
from LenmoTest.serializers.user_serializer import UserSerializer, UserBalanceSerializer
from db.models import User


class AuthenticationMixin(object):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


def create_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')


class Login(GenericAPIView):
    """
    use it to get user token to Authorize your operations

    """
    serializer_class = JSONWebTokenSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        token = create_token(user)
        model = UserSerializer(user, context={"request": request})
        return Response({'token': token, 'user': model.data})


class Register(CreateAPIView):
    """
    NOTE :
    USER TYPES : [ BORROWER , INVESTOR ] \n
    USER GENDER : [ MALE , FEMALE ]
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": "request"})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        token = create_token(user)
        data = {'object': UserSerializer(user, context={"request": request}).data, 'token': token}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



