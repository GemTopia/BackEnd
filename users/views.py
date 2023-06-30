from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer
from rest_framework import status

class UserRegistration(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)

        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data,request.POST['referrer_code'])
            return Response(ser_data.validated_data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


