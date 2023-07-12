from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistration(APIView):
<<<<<<< HEAD
    serializer_class = UserRegisterSerializer

    def post(self, request):
        print(request.body)
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(validated_data=ser_data.validated_data, referrer_code=request.data.get('referrer_code'))
=======
    """"
        Registration
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)

        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data, request.POST['referrer_code'])

>>>>>>> b9b6c554b6b28b3004e873a25b252b989c998045
            data = {'email': request.data['email'], 'password': request.data['password']}
            response = TokenObtainPairView.as_view()(request._request, data=data)
            return response

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
