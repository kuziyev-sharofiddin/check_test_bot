# Generated by Django 4.1.5 on 2023-02-07 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu_bot', '0010_testresponse_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresponse',
            name='group',
        ),
    ]