# Generated by Django 4.0.6 on 2022-08-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_imagemetadata_height_alter_imagemetadata_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemetadata',
            name='format',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='mode',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
