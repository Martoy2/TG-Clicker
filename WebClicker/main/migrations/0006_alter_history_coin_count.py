# Generated by Django 5.0.6 on 2024-06-23 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='coin_count',
            field=models.FloatField(),
        ),
    ]
