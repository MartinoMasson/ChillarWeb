# Generated by Django 5.1.6 on 2025-03-07 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChillarWeb', '0002_remove_cliente_trabajo_proyecto_cliente_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('texto', models.TextField()),
                ('imagen', models.ImageField(upload_to='imagenes/')),
            ],
        ),
    ]
