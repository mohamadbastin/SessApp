# Generated by Django 2.2.1 on 2019-09-12 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sess_app', '0015_privacypolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_text', models.CharField(max_length=1000)),
                ('telegram', models.CharField(max_length=100)),
                ('whatsapp', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
            ],
        ),
    ]
