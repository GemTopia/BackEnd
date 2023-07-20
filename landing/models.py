from django.db import models
from datetime import datetime, timedelta


class GemytoInfo(models.Model):
    token_value = models.JSONField()
    created_at = models.DateTimeField()


    class Meta:
        db_table = 'gemyto_info'
        ordering = ['created_at']
 
class EmailForNews(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_news'
