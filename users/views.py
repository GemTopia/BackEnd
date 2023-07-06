from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer, UserSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from users.models import User
from django.shortcuts import get_object_or_404


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
    
class UserViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        ser_data = self.serializer_class(instance=user)
        if user.played_game:
            return Response(ser_data.data)
        ser_data.data.pop('user_games', None)
        return Response(ser_data.data)


    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk) 
        # if user == request.user:
        ser_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        # return Response({'Permission denied': 'You can not edit other profiles'}, status=status.HTTP_401_UNAUTHORIZED)


