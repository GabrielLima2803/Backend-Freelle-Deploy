# Generated by Django 5.0.6 on 2024-08-03 20:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_projeto_orcamento_projeto_proposta_recebida_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProjeto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "client_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "freelancer_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="freelancer_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "projeto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="user_projects", to="core.projeto"
                    ),
                ),
            ],
            options={
                "verbose_name": "User Projeto",
                "verbose_name_plural": "User Projetos",
                "unique_together": {("client_user", "freelancer_user", "projeto")},
            },
        ),
    ]
