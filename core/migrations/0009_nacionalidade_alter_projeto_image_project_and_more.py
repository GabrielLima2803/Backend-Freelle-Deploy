# Generated by Django 5.0.6 on 2024-09-02 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_user_reset_code_alter_user_passage_id"),
        ("uploader", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Nacionalidade",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, unique=True)),
                ("sigla", models.CharField(max_length=2)),
            ],
            options={
                "verbose_name": "Nacionalidade",
                "verbose_name_plural": "Nacionalidades",
            },
        ),
        migrations.AlterField(
            model_name="projeto",
            name="image_project",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="uploader.image",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="uploader.image",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="nacionalidade",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="users",
                to="core.nacionalidade",
            ),
        ),
    ]
