# Generated by Django 2.1.2 on 2019-03-01 02:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0033_auto_20190228_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=20)),
                ('descuento', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Productos')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Envio_Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_recibe', models.CharField(max_length=20)),
                ('apellido_p', models.CharField(max_length=20)),
                ('apellido_m', models.CharField(max_length=20)),
                ('calle', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=10)),
                ('cp', models.CharField(max_length=10)),
                ('municipio', models.CharField(default='', max_length=50)),
                ('estado', models.CharField(default='', max_length=50)),
                ('pais', models.CharField(default='', max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('correo_electronico', models.CharField(max_length=50)),
                ('referencia', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=datetime.datetime(2019, 2, 28, 20, 48, 14, 864573))),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.AddField(
            model_name='direccion_envio_venta',
            name='id_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.Venta'),
        ),
        migrations.AddField(
            model_name='detalle_venta',
            name='id_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.Venta'),
        ),
        migrations.AddField(
            model_name='detalle_venta',
            name='talla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Tallas'),
        ),
    ]
