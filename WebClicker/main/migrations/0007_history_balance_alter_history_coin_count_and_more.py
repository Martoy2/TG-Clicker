# Generated by Django 5.0.6 on 2024-06-24 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_history_coin_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='history',
            name='coin_count',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='click',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
    ]
