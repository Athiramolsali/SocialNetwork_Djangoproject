# Generated by Django 4.2.6 on 2024-09-08 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='created_at',
            new_name='time',
        ),
    ]
