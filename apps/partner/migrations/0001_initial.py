# Generated by Django 4.2.9 on 2024-01-07 16:50

from django.db import migrations, models
import django.db.models.deletion
import hitcount.models
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnerHome",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "short_description",
                    models.TextField(blank=True, null=True, verbose_name="간략한 설명"),
                ),
                (
                    "content",
                    wagtail.fields.StreamField(
                        [
                            (
                                "banner",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "slides",
                                            wagtail.blocks.StreamBlock(
                                                [
                                                    (
                                                        "slide",
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "image",
                                                                    wagtail.images.blocks.ImageChooserBlock(
                                                                        label="이미지"
                                                                    ),
                                                                ),
                                                                (
                                                                    "description",
                                                                    wagtail.blocks.RawHTMLBlock(
                                                                        label="HTML",
                                                                        required=False,
                                                                    ),
                                                                ),
                                                            ],
                                                            label="슬라이드",
                                                        ),
                                                    )
                                                ],
                                                collapsed=True,
                                                label="슬라이드",
                                            ),
                                        ),
                                        (
                                            "height",
                                            wagtail.blocks.ChoiceBlock(
                                                choices=[
                                                    ("300", "300px"),
                                                    ("400", "400px"),
                                                    ("500", "500px"),
                                                    ("600", "600px"),
                                                    ("700", "700px"),
                                                    ("800", "800px"),
                                                ],
                                                label="슬라이더 높이 px",
                                            ),
                                        ),
                                        (
                                            "fit_container",
                                            wagtail.blocks.BooleanBlock(
                                                label="container에 맞추기", required=False
                                            ),
                                        ),
                                    ],
                                    label="배너",
                                    required=False,
                                ),
                            ),
                            (
                                "richtext",
                                wagtail.blocks.RichTextBlock(
                                    label="에디터", required=False
                                ),
                            ),
                            (
                                "html",
                                wagtail.blocks.RawHTMLBlock(
                                    label="HTML 코드", required=False
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                        use_json_field=True,
                        verbose_name="내용",
                    ),
                ),
                (
                    "cover",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.image",
                        verbose_name="커버",
                    ),
                ),
            ],
            options={
                "verbose_name": "파트너",
                "verbose_name_plural": "파트너",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "content",
                    wagtail.fields.StreamField(
                        [
                            (
                                "banner",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "slides",
                                            wagtail.blocks.StreamBlock(
                                                [
                                                    (
                                                        "slide",
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "image",
                                                                    wagtail.images.blocks.ImageChooserBlock(
                                                                        label="이미지"
                                                                    ),
                                                                ),
                                                                (
                                                                    "description",
                                                                    wagtail.blocks.RawHTMLBlock(
                                                                        label="HTML",
                                                                        required=False,
                                                                    ),
                                                                ),
                                                            ],
                                                            label="슬라이드",
                                                        ),
                                                    )
                                                ],
                                                collapsed=True,
                                                label="슬라이드",
                                            ),
                                        ),
                                        (
                                            "height",
                                            wagtail.blocks.ChoiceBlock(
                                                choices=[
                                                    ("300", "300px"),
                                                    ("400", "400px"),
                                                    ("500", "500px"),
                                                    ("600", "600px"),
                                                    ("700", "700px"),
                                                    ("800", "800px"),
                                                ],
                                                label="슬라이더 높이 px",
                                            ),
                                        ),
                                        (
                                            "fit_container",
                                            wagtail.blocks.BooleanBlock(
                                                label="container에 맞추기", required=False
                                            ),
                                        ),
                                    ],
                                    label="배너",
                                    required=False,
                                ),
                            ),
                            (
                                "richtext",
                                wagtail.blocks.RichTextBlock(
                                    label="에디터", required=False
                                ),
                            ),
                            (
                                "html",
                                wagtail.blocks.RawHTMLBlock(
                                    label="HTML 코드", required=False
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                        use_json_field=True,
                        verbose_name="내용",
                    ),
                ),
                ("priority", models.IntegerField(default=0, verbose_name="상단 정렬")),
                (
                    "external_link",
                    models.URLField(
                        blank=True, max_length=254, null=True, verbose_name="외부 링크"
                    ),
                ),
                (
                    "allow_rating",
                    models.BooleanField(default=False, verbose_name="추천 사용하기"),
                ),
                (
                    "allow_comments",
                    models.BooleanField(default=False, verbose_name="댓글 사용하기"),
                ),
                (
                    "categories",
                    modelcluster.fields.ParentalManyToManyField(
                        blank=True, to="base.category", verbose_name="카테고리"
                    ),
                ),
                (
                    "logo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.image",
                        verbose_name="로고",
                    ),
                ),
                (
                    "tags",
                    modelcluster.contrib.taggit.ClusterTaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="base.TaggedPageItem",
                        to="base.Tag",
                        verbose_name="태그",
                    ),
                ),
            ],
            options={
                "verbose_name": "파트너",
                "verbose_name_plural": "파트너",
            },
            bases=("wagtailcore.page", hitcount.models.HitCountMixin),
        ),
    ]
