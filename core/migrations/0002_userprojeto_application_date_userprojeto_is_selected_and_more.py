# Generated by Django 5.0.6 on 2024-12-08 23:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprojeto",
            name="application_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="userprojeto",
            name="is_selected",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprojeto",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Pendente"), (2, "Rejeitado"), (3, "Selecionado"), (4, "Não selecionado")], default=1
            ),
        ),
    ]