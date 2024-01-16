# Generated by Django 4.2.9 on 2024-01-12 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("blog", "0002_blog_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="thumbnail",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wagtailimages.image",
                verbose_name="섬네일",
            ),
        ),
    ]