# Generated by Django 3.2.8 on 2021-11-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_job_accepter'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='lat_lng',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
