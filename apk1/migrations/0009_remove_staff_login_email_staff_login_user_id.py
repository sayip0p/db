# Generated by Django 5.1.5 on 2025-06-02 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk1', '0008_staff_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff_login',
            name='email',
        ),
        migrations.AddField(
            model_name='staff_login',
            name='user_id',
            field=models.CharField(default='staff001', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
