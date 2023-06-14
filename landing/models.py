from django.db import models


class GemytoInfo(models.Model):
    token_value = models.PositiveIntegerField()

    class Meta:
        db_table = 'gemyto_info'
