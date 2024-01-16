from django.db.models import SET_NULL, ForeignKey
from wagtail import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import RichTextBlock
from wagtail.contrib.forms.models import AbstractForm
from wagtail.fields import StreamField
from wagtail.models import Orderable, ParentalKey

from apps.base.forms import NormalizedFormBuilder
from apps.base.models import AbstractPageHome, AbstractDetailPage

class BlogHome(AbstractPageHome):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    subpage_types = ["Blog"]

    def get_template(self, request, *args, **kwargs):
        return "blog/blog_home.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blogpages'] = self.get_children().live()
        return context

class Blog(AbstractDetailPage):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    parent_page_types = ["BlogHome"]
    subpage_types = []

    subtitle = StreamField(
        [
            ("subtitle", RichTextBlock(label="에디터", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="소제목",
        use_json_field=True,
    )

    content_panels = AbstractDetailPage.content_panels + [
        InlinePanel('thumbnail_images', label='Thumbnail Images'),
        FieldPanel("subtitle"),
    ]

    def main_image(self):
        thumbnail_item = self.thumbnail_images.first()
        if thumbnail_item:
            return thumbnail_item.thumbnail
        else:
            return None

    def get_template(self, request, *args, **kwargs):
        return "blog/blog.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

class BlogPageThumbnailImage(Orderable):
    blog = ParentalKey(Blog, null=True, blank=True, on_delete=SET_NULL, related_name='thumbnail_images')
    thumbnail = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, verbose_name="섬네일")

    panels = [
        FieldPanel('thumbnail'),
    ]
