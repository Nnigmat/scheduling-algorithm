# Generated by Django 2.1.7 on 2019-04-01 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_schedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='faculties',
        ),
        migrations.RemoveField(
            model_name='course',
            name='n_lab',
        ),
        migrations.RemoveField(
            model_name='course',
            name='n_lecture',
        ),
        migrations.AddField(
            model_name='course',
            name='class_num',
            field=models.IntegerField(default=100, max_length=1000, verbose_name='Number of classes'),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(default=2019, max_length=3000),
        ),
        migrations.AddField(
            model_name='faculty',
            name='type',
            field=models.CharField(default='TA', max_length=50, verbose_name='Type'),
            preserve_default=False,
        ),
    ]
