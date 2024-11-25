# Generated by Django 4.1.5 on 2024-11-25 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuqrcode_menu_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='MongoMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postgres_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tags', models.CharField(max_length=255)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
            ],
            options={
                'db_table': 'menu_mongo',
            },
        ),
    ]