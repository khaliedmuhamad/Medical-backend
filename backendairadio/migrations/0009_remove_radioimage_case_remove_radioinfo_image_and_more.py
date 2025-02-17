# Generated by Django 5.0.6 on 2024-06-07 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendairadio', '0008_remove_radioimage_körper_teil_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radioimage',
            name='case',
        ),
        migrations.RemoveField(
            model_name='radioinfo',
            name='image',
        ),
        migrations.AddField(
            model_name='radioimage',
            name='radio_Info',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='backendairadio.radioinfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='radioinfo',
            name='case',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='backendairadio.case'),
            preserve_default=False,
        ),
    ]
