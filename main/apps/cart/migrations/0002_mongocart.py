# Generated by Django 4.1.5 on 2024-11-25 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MongoCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postgres_id', models.IntegerField(unique=True)),
                ('user_id', models.IntegerField()),
                ('menu_item_id', models.IntegerField()),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
