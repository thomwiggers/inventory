# Generated by Django 2.2.6 on 2019-10-08 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_auto_20190929_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brandean',
            old_name='brand_label',
            new_name='label',
        ),
    ]