# Generated by Django 4.2.9 on 2024-01-10 08:32

from django.db import migrations, models
import wagtail.search.index


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NcsClassification",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                        verbose_name="분류 코드",
                    ),
                ),
                ("class1_code", models.CharField(max_length=10, verbose_name="대분류 코드")),
                (
                    "class1_name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="대분류 명칭"
                    ),
                ),
                ("class2_code", models.CharField(max_length=10, verbose_name="중분류 코드")),
                (
                    "class2_name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="중분류 명칭"
                    ),
                ),
                ("class3_code", models.CharField(max_length=10, verbose_name="소분류 코드")),
                (
                    "class3_name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="소분류 명칭"
                    ),
                ),
            ],
            options={
                "verbose_name": "ncs 분류",
                "verbose_name_plural": "ncs 분류",
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]