# Generated by Django 5.0.6 on 2024-06-04 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendairadio', '0004_alter_radioinfo_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radioinfo',
            name='size',
        ),
    ]
