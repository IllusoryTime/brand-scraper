# Generated by Django 4.0.6 on 2022-08-04 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_imagemetadata_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
