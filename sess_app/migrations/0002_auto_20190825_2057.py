# Generated by Django 2.2.1 on 2019-08-25 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sess_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('user_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='sess_app.UserCourse')),
            ],
        ),
        migrations.CreateModel(
            name='ExamDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('date', models.CharField(max_length=1000)),
                ('grade', models.IntegerField()),
                ('user_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_dates', to='sess_app.UserCourse')),
            ],
        ),
    ]
