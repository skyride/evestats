# Generated by Django 2.0.7 on 2018-07-20 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0031_auto_20180720_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributetype',
            name='icon_id',
        ),
        migrations.AddField(
            model_name='attributetype',
            name='icon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sde.Icon'),
        ),
    ]
