# Generated by Django 2.2.5 on 2019-09-29 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packaging',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='interface.Product'),
            preserve_default=False,
        ),
    ]
