# Generated by Django 5.0.6 on 2024-08-13 19:50

import core.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_userprojeto_client_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="reset_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="passage_id",
            field=models.CharField(default=core.models.user.generate_unique_passage_id, max_length=255, unique=True),
        ),
    ]