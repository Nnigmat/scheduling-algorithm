# Generated by Django 2.1.7 on 2019-04-18 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferences',
            old_name='classes_row',
            new_name='classes_in_row',
        ),
        migrations.RenameField(
            model_name='preferences',
            old_name='classes_day',
            new_name='classes_per_day',
        ),
    ]
