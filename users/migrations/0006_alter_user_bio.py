# Generated by Django 4.2.2 on 2023-07-05 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_socialmedia_delete_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
