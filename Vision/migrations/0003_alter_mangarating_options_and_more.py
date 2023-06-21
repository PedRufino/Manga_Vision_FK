# Generated by Django 4.1.6 on 2023-06-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Vision", "0002_remove_mangas_type_manga"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mangarating",
            options={"ordering": ["manga"]},
        ),
        migrations.RemoveField(
            model_name="mangarating",
            name="created_at",
        ),
        migrations.AddField(
            model_name="mangarating",
            name="total",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="mangarating",
            name="rating",
            field=models.IntegerField(default=0),
        ),
    ]