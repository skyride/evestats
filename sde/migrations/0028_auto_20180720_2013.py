# Generated by Django 2.0.7 on 2018-07-20 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0027_auto_20180720_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skinlicense',
            name='type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='sde.Type'),
        ),
    ]
