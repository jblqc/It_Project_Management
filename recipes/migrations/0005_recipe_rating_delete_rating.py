# Generated by Django 4.2 on 2023-05-14 04:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0004_remove_recipe_rating_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="Rating",
        ),
    ]
