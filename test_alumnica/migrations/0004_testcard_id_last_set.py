# Generated by Django 2.2.3 on 2019-07-16 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_alumnica', '0003_auto_20190712_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcard',
            name='id_last_set',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
