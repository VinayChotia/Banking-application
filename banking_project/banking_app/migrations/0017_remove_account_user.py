# Generated by Django 5.0.7 on 2024-07-30 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0016_account_user_alter_user_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
    ]
