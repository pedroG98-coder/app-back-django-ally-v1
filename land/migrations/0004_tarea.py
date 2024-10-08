# Generated by Django 4.2.15 on 2024-10-07 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0003_user_foto_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tarea', models.CharField(help_text='Nombre Tarea', max_length=255)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción de la tarea')),
                ('fecha_vencimiento', models.DateTimeField(blank=True, help_text='Fecha límite para completar la tarea', null=True)),
                ('prioridad', models.IntegerField(choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')], default=2, help_text='Nivel de prioridad de la tarea')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', help_text='Estado actual de la tarea', max_length=50)),
                ('estatus_sistema', models.BooleanField(default=True, help_text='True si está activo, False si está eliminado.', verbose_name='Estatus en el Sistema')),
                ('fecha_elaboracion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
