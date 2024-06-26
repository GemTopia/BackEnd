# Generated by Django 4.2.2 on 2023-07-25 16:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import game.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPlayedGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('state', models.PositiveIntegerField(choices=[(1, 'State 1'), (2, 'State 2'), (3, 'State 3'), (4, 'State 4')], default=0)),
                ('game_gemyto', models.FloatField(default=0)),
                ('is_new_record', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'verbose_name': ' daily  played game',
                'verbose_name_plural': 'daily played games',
                'db_table': 'daily_played_game',
                'ordering': ['score'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('name', models.CharField(max_length=200)),
                ('link', models.URLField(null=True)),
                ('rank', models.PositiveIntegerField(default=0, editable=False)),
                ('num_of_like', models.PositiveIntegerField(default=0, editable=False)),
                ('num_of_report', models.PositiveIntegerField(default=0)),
                ('game_type', models.CharField(choices=[('action', 'action'), ('shooting', 'shooting'), ('quiz', 'quiz'), ('sport', 'sport'), ('puzzle', 'puzzle')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to=game.models.game_picture_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), game.models.validate_image_size])),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to=game.models.game_picture_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), game.models.validate_image_size])),
                ('num_of_users_get_gemyto', models.PositiveIntegerField(blank=True, default=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'game',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='GamePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=game.models.game_picture_directory_path)),
            ],
            options={
                'db_table': 'game_picture',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'like',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PlayedGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_gemyto', models.FloatField(default=0)),
                ('score', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'played game',
                'verbose_name_plural': 'played games',
                'db_table': 'played_game',
                'ordering': ['score'],
            },
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_value', models.PositiveIntegerField(default=0)),
                ('first_level_score', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('second_level_score', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('third_level_score', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('fourth_level_score', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('distance', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'scores',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_text', models.TextField()),
                ('validate', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_reports', to='game.game')),
            ],
            options={
                'db_table': 'report',
                'ordering': ['created_at'],
            },
        ),
    ]
