# Generated by Django 3.2 on 2021-04-26 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doge',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ts', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('price', models.DecimalField(decimal_places=65535, max_digits=65535)),
            ],
            options={
                'db_table': 'doge',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('tweet', models.TextField()),
            ],
            options={
                'db_table': 'tweets',
                'managed': False,
            },
        ),
    ]
