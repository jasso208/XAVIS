# Generated by Django 2.1.2 on 2019-03-06 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0035_auto_20190301_0015'),
        ('blog', '0004_auto_20190304_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos_Relacionados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_blog', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='blog', to='blog.Blog')),
                ('id_producto_relacionado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='id_producto_relacionado', to='inventario.Productos')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='productos_relacionados',
            unique_together={('id_blog', 'id_producto_relacionado')},
        ),
    ]
