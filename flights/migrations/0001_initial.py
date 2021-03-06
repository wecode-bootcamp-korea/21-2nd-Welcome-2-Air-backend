# Generated by Django 3.2.4 on 2021-06-22 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('airport_code', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=20)),
                ('departure_date', models.DateField()),
                ('arrival_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField(max_length=20)),
                ('duration', models.TimeField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('arrival_city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival', to='flights.city')),
                ('departure_city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure', to='flights.city')),
            ],
            options={
                'db_table': 'flights',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
                ('price_ratio', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'seats',
            },
        ),
        migrations.CreateModel(
            name='FlightSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='air_seat', to='flights.flight')),
                ('seat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.seat')),
            ],
            options={
                'db_table': 'flight_seats',
            },
        ),
        migrations.AddField(
            model_name='flight',
            name='flight_seat',
            field=models.ManyToManyField(through='flights.FlightSeat', to='flights.Seat'),
        ),
        migrations.AddField(
            model_name='city',
            name='country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.country'),
        ),
    ]
