from django.utils.translation import gettext_lazy
from drf_spectacular.utils import extend_schema
from accounts.serializers.user import RegisterSerializer,LoginSerializer
from common.serializer import UserVerificationMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from defender import utils as defender_utils
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import AllowAny, IsAuthenticated

@extend_schema(tags=["User Authentication"], summary="User signup", request=RegisterSerializer)
class UserSignUp(APIView):
    """
    For user signup.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp = UserVerificationMessageSerializer(
            instance=dict(
                detail=gettext_lazy("Successfully signed up"),
            )
        )
        return Response(resp.data, status=status.HTTP_201_CREATED)
    
    
@extend_schema(tags=["User Authentication"], summary="User Login", request=LoginSerializer)
class LoginView(KnoxLoginView):
    """
        This API is used to login the user. \n
        The username and password must be passed in the request body.
    """
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Login the user.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        defender_utils.reset_failed_attempts(request, 'login')
        token = AuthToken.objects.create(serializer.validated_data['user'])[1]


        return Response(token, status=status.HTTP_200_OK)