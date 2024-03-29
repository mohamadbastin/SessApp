# Generated by Django 2.2.1 on 2019-08-28 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sess_app', '0005_auto_20190826_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='profiles',
            field=models.ManyToManyField(through='sess_app.UserCourse', to='sess_app.Profile'),
        ),
        migrations.AddField(
            model_name='department',
            name='name',
            field=models.CharField(default='z', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='picture',
            field=models.ImageField(default='1', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='courses',
            field=models.ManyToManyField(through='sess_app.UserCourse', to='sess_app.Course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='cs_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='sess_app.Department'),
        ),
        migrations.AlterField(
            model_name='department',
            name='dep_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course', to='sess_app.Course'),
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course', to='sess_app.Profile'),
        ),
    ]
