# Generated by Django 5.0.7 on 2024-07-29 11:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0005_remove_account_user_user_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_number',
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
