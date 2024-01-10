# Generated by Django 4.2.9 on 2024-01-10 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ncs", "0001_initial"),
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="hrdnet_code",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="hrdnet 코드"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="mobile",
            field=models.BooleanField(default=True, verbose_name="모바일"),
        ),
        migrations.AlterField(
            model_name="course",
            name="ncs_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ncs.ncsclassification",
                verbose_name="NCS 분류",
            ),
        ),
    ]