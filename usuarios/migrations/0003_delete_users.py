# Generated by Django 4.0.4 on 2022-04-23 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_users_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]