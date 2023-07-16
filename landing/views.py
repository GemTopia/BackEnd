from rest_framework import viewsets
from django.core.mail import send_mail
from .models import News
from .serializers import NewsSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Send email to the user
        News = self.get_object()
        send_mail(
            'Subject',
            'Text',
            'from@example.com',
            [News.email],
            fail_silently=False,
        )
        
        return response

# more information about send email

# https://docs.djangoproject.com/en/3.2/topics/email/