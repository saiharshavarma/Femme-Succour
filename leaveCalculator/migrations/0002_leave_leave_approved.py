# Generated by Django 4.1.7 on 2023-03-05 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveCalculator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leave_approved',
            field=models.BooleanField(default=False),
        ),
    ]
