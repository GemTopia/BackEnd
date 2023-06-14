from django.db import models


def game_master_avatar_directory_path(instance, filename):
    return 'game_master/{0}/avatar/{1}'.format(str(instance.username), filename)


class GameMaster(models.Model):
    username = models.CharField(max_length=50)
    information = models.TextField()
    avatar = models.ImageField(upload_to=game_master_avatar_directory_path, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['created_at']
        verbose_name = 'game master'
        verbose_name_plural = 'game masters'
