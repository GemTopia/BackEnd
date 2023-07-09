from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer, UserSerializer,SocialMediaSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from users.models import User,SocialMedia
from django.shortcuts import get_object_or_404
from game.models import PlayedGame
from game.serializers import DailyPlayedGameSerializer
from rest_framework import viewsets
import re



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
    
class ProfileView(APIView):

    serializer_class = UserSerializer

    def get(self, request):
        user=request.user
        wnated_user = User.objects.get(user_name=request.GET.get('user',''))
        if wnated_user:
            if user==wnated_user:
                ser_data = self.serializer_class(instance=wnated_user)
                
                return Response(ser_data.data)
            else:
                ser_data = self.serializer_class(instance=wnated_user)
                copy_of_data=ser_data.data 
                copy_of_data.pop('email')
                copy_of_data.pop('hide_button') 
                copy_of_data.pop('referrer_code')
                if not wnated_user.hide_button:
                    return Response(copy_of_data)
                else:
                    a.pop('user_games')
                    return Response(copy_of_data)
        return Response('there is not any user whit this user_name')

    def put(self, request ):
        user = request.user
        ser_data = UserSerializer(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)



        

def is_profile_url(url, platform):
    if platform == 'instagram':
        pattern = r'^https?://(www\.)?instagram\.com/([a-zA-Z0-9_]+)$'
    elif platform == 'telegram':
        pattern = r'^https?://(www\.)?t\.me/([a-zA-Z0-9_]+)$'
    elif platform == 'twitch':
        pattern = r'^https?://(www\.)?twitch\.tv/([a-zA-Z0-9_]+)$'
    elif platform == 'discord':
        pattern = r'^https?://(www\.)?discord(app)?\.com/users/([0-9]+)$'
    elif platform == 'youtube':
        pattern = r'^https?://(www\.)?youtube\.com/(user/|channel/)([a-zA-Z0-9_\-]+)$'
    elif platform == 'steam':
        pattern = r'^https?://(www\.)?steamcommunity\.com/(id|profiles)/([a-zA-Z0-9_]+)$'
    else:
        return False
    return re.match(pattern, url) is not None

class LinkView(APIView):

    def put(self, request):

        socials=["telegram","instagram","twitch","steam","youtube","discord"]
        userID = request.user
        error=[]
        
        for i in socials:
            data={'name':i,"link":request.data.get(i)}
            if (request.data.get(i) and is_profile_url(request.data.get(i),i)) or not request.data.get(i):
                if SocialMedia.objects.filter(user=userID,name=i).exists():
                    instanc=SocialMedia.objects.get(user=userID,name=i)
                    ser_data = SocialMediaSerializer(instance=instanc,data=data, partial=True)
                    if ser_data.is_valid():
                        ser_data.save()
                    else:
                        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    ser_data=SocialMediaSerializer(data=data)
                    if ser_data.is_valid():
                        ser_data.validated_data["user_id"]=request.user.id
                        SocialMedia.objects.create(**ser_data.validated_data)
                    else:
                        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                error.append(i)
        error_text=""
        if error:
            for i in error:
                error_text+=i+","
            return Response({"status":"the url of "+error_text+" is wrong"})
        else:
            return Response({"status":"done"})
