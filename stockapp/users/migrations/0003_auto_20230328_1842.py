# Generated by Django 3.2.18 on 2023-03-28 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230327_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='usersstock',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]
