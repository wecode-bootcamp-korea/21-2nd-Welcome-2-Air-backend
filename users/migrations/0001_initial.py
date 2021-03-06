# Generated by Django 3.2.4 on 2021-06-22 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=45)),
                ('name_kor', models.CharField(max_length=45)),
                ('name_eng', models.CharField(max_length=45)),
                ('birth', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('gender', models.BooleanField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
