from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegistration(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data, request.POST['referrer_code'])
            
            data = {'email': request.data['email'], 'password': request.data['password']}
            token_obtain_pair_view = TokenObtainPairView.as_view()
            response = token_obtain_pair_view(request._request, data=data)
            return response

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

