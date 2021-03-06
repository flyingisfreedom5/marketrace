# Generated by Django 4.0.3 on 2022-05-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_bucket_numstocks_stockinstance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-mr_volume']},
        ),
        migrations.AlterField(
            model_name='stock',
            name='mr_close',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stockinstance',
            name='price',
            field=models.FloatField(),
        ),
    ]
