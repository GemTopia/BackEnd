from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer, UserSerializer, SocialMediaSerializer, ChangePasswordSerializer
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User, SocialMedia
from utils import is_profile_url
from rest_framework.permissions import IsAuthenticated



class UserRegistration(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
<<<<<<< HEAD
        request.body
=======
        print(request.body)
>>>>>>> main
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(validated_data=ser_data.validated_data, referrer_code=request.data.get('referrer_code'))
            data = {'email': request.data['email'], 'password': request.data['password']}
            response = TokenObtainPairView.as_view()(request._request, data=data)
            return response

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
<<<<<<< HEAD


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        wanted_user = User.objects.get(user_name=request.GET.get('user', ''))
        if wanted_user:
            if user == wanted_user:
                ser_data = self.serializer_class(instance=wanted_user)
                return Response(ser_data.data)
            else:
                ser_data = self.serializer_class(instance=wanted_user)
                copy_of_data = ser_data.data
                copy_of_data.pop('email')
                copy_of_data.pop('hide_button')
                copy_of_data.pop('referrer_code')
                if not wanted_user.hide_button:
                    return Response(copy_of_data)
                else:
                    copy_of_data.pop('user_games')
                    return Response(copy_of_data)
        return Response('There is not any user with this username')

    def put(self, request):
        user = request.user
        ser_data = UserSerializer(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SocialMediaSerializer

    def put(self, request):
        socials = ["telegram", "instagram", "twitch", "steam", "youtube", "discord"]
        userID = request.user
        error = []

        for i in socials:
            data = {'name': i, "link": request.data.get(i)}
            if (request.data.get(i) and is_profile_url(request.data.get(i), i)) or not request.data.get(i):
                if SocialMedia.objects.filter(user=userID, name=i).exists():
                    instance = SocialMedia.objects.get(user=userID, name=i)
                    ser_data = self.serializer_class(instance=instance, data=data, partial=True)
                    if ser_data.is_valid():
                        ser_data.save()
                    else:
                        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    ser_data = self.serializer_class(data=data)
                    if ser_data.is_valid():
                        ser_data.validated_data["user_id"] = request.user.id
                        SocialMedia.objects.create(**ser_data.validated_data)
                    else:
                        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                error.append(i)
        error_text = ""
        if error:
            for i in error:
                error_text += i + ","
            return Response({"status": "The url of " + error_text + " is wrong"})
        else:
            return Response({"status": status.HTTP_200_OK})


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data, context={'request': request})
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
            return Response('Password updated successfully', status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


=======
>>>>>>> main
