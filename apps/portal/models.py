from django.apps import apps
from django.conf import settings
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.base.blocks import BannerBlock, PageContentBlock


class Portal(Page):
    class Meta:
        verbose_name = "포털"
        verbose_name_plural = verbose_name

    content = StreamField(
        [
            ("banner", BannerBlock(label="배너", required=False)),
            (
                "page_content",
                StreamBlock(
                    [
                        ("page_content", PageContentBlock(label="페이지 콘텐츠")),
                    ],
                    label="페이지 콘텐츠",
                ),
            ),
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="페이지 내용",
        use_json_field=True,
    )

    footer = StreamField(
        [
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="푸터",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
        FieldPanel("footer"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # site content
        for content_block in self.content:
            if content_block.block_type == "page_content":
                for page_content_block in content_block.value:
                    app_label, model_name = page_content_block.value["model_string"].split(".")
                    page_content_homes = (
                        self.get_children()
                        .live()
                        .filter(
                            content_type__app_label=app_label,
                            content_type__model=model_name.lower(),
                        )
                    )

                    if not page_content_homes:
                        continue

                    # filter by tag
                    page_content = Page.objects.none()
                    for page_content_home in page_content_homes:
                        page_content = page_content.union(
                            page_content_home.get_children().live().order_by("-id")
                        )

                    tag = page_content_block.value["tag"]
                    if tag:
                        page_content = page_content.filter(taggedpageitem__tag__name=tag)

                    # limit count. default 4, max 8
                    count = min(page_content_block.value["count"] or 4, 8)
                    page_content_block.value["page_content"] = page_content.distinct()[:count]
                    page_content_block.value["page_content_home"] = page_content_homes.first()

        return context
