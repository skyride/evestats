# Generated by Django 2.0.7 on 2018-07-20 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0028_auto_20180720_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skinlicense',
            name='type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skin_license', to='sde.Type'),
        ),
    ]
