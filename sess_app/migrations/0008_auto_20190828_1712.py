# Generated by Django 2.2.1 on 2019-08-28 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sess_app', '0007_auto_20190828_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='profiles',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='courses',
        ),
    ]
