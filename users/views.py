from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistration(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        request.body

        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(validated_data=ser_data.validated_data, referrer_code=request.data.get('referrer_code'))
            data = {'email': request.data['email'], 'password': request.data['password']}
            response = TokenObtainPairView.as_view()(request._request, data=data)
            return response

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

