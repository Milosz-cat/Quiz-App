# Generated by Django 4.1.3 on 2023-03-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0009_answer_is_confirmed_question_is_confirmed_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="description",
            field=models.CharField(max_length=250),
        ),
    ]
