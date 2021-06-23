# Generated by Django 3.2.4 on 2021-06-23 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='name_eng',
            new_name='english_name',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='name_kor',
            new_name='korean_name',
        ),
        migrations.AddField(
            model_name='passenger',
            name='passport_number',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='passenger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_air', to='tickets.passenger'),
        ),
    ]