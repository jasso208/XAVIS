# Generated by Django 2.2.6 on 2020-07-31 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empenos', '0084_auto_20200730_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='abono',
            name='folio',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='abono',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='empenos.Sucursal'),
        ),
        migrations.AddField(
            model_name='abono',
            name='tipo_movimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='empenos.Tipo_Movimiento'),
        ),
    ]
