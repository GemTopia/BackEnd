# Generated by Django 4.2.2 on 2023-07-04 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_bio_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]