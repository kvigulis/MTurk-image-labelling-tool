# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_labelling_tool', '0003_auto_20180226_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageWithLabels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('labels', models.OneToOneField(related_name='image', to='image_labelling_tool.Labels')),
            ],
        ),
    ]
