# Generated by Django 3.0.3 on 2020-02-09 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20200208_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='favorite',
            field=models.BooleanField(default=False, null=True),
        ),
    ]