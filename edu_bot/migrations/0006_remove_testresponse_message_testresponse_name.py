# Generated by Django 4.1.5 on 2023-02-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu_bot', '0005_alter_testresponse_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresponse',
            name='message',
        ),
        migrations.AddField(
            model_name='testresponse',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]