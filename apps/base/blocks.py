from django.conf import settings
from wagtail.blocks import (
    BooleanBlock,
    ChoiceBlock,
    IntegerBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageChooserBlock


def tag_choices():
    from apps.base.models import Tag

    return [
        choice
        for choice in Tag.objects.exclude(
            # **{f"{TaggedPageItem.tag_relname()}__content_object__content_type__isnull": True}
        )
        .values_list("name", "name")
        .distinct()
    ]


class PageContentBlock(StructBlock):
    """PageContentBlock."""

    class Meta:
        """Meta."""

    # fmt: off

    model_string = ChoiceBlock(label="콘텐츠 타입", choices=settings.PAGE_CONTENT)
    tag = ChoiceBlock(label="태그", choices=tag_choices, required=False, help_text="공란이면 최신 순으로 가져옵니다.")
    count = IntegerBlock(label="콘텐츠 수", default=8)
    description = RichTextBlock(required=False, label="설명")
    icon = ImageChooserBlock(required=False, label="아이콘")

    # fmt: on


class BannerBlock(StructBlock):
    class Meta:
        label = "배너"

    slides = StreamBlock(
        [
            (
                "slide",
                StructBlock(
                    [
                        ("image", ImageChooserBlock(label="이미지")),
                        ("description", RawHTMLBlock(label="HTML", required=False)),
                    ],
                    label="슬라이드",
                ),
            )
        ],
        collapsed=True,
        label="슬라이드",
    )
    height = ChoiceBlock(
        label="슬라이더 높이 px",
        default="400",
        choices=(
            ("300", "300px"),
            ("400", "400px"),
            ("500", "500px"),
            ("600", "600px"),
            ("700", "700px"),
            ("800", "800px"),
        ),
    )
    fit_container = BooleanBlock(label="container에 맞추기", required=False)
