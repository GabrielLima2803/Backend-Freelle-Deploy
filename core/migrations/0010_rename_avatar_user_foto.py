# Generated by Django 5.0.6 on 2024-09-10 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_nacionalidade_alter_projeto_image_project_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="avatar",
            new_name="foto",
        ),
    ]