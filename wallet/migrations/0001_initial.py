# Generated by Django 4.2.2 on 2023-07-21 06:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_address', models.CharField(max_length=42)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wallet',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_wallet', models.CharField(max_length=42)),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_wallet', to='wallet.wallet')),
            ],
            options={
                'db_table': 'transaction',
                'ordering': ['created_at'],
            },
        ),
    ]
