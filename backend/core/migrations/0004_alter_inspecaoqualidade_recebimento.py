# Generated by Django 5.2.3 on 2025-06-15 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_defeito_inspecaoqualidade_iteminspecionadodefeito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspecaoqualidade',
            name='recebimento',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inspecao', to='core.recebimento', verbose_name='Recebimento Inspecionado'),
        ),
    ]
