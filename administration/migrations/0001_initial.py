# Generated by Django 4.2.7 on 2023-11-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bm_1', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bm_2', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bm_3', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bs_1', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bs_2', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bs_3', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('bs_4', models.ImageField(blank=True, null=True, upload_to='banners')),
            ],
        ),
    ]
