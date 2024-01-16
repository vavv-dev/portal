from django.db.models import CASCADE, ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from apps.base.models import AbstractPageHome, AbstractDetailPage


class IndustryHome(AbstractPageHome):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    subpage_types = ["Industry"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['industries'] = self.get_children().live()
        return context


    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

class Industry(AbstractDetailPage):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    parent_page_types = ["IndustryHome"]
    subpage_types = []

    content_panels = AbstractDetailPage.content_panels + [
        InlinePanel("images", label="이미지"),
    ]

    def main_image(self):
        gallery_item = self.images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


class IndustryImage(Orderable):
    industry = ParentalKey("Industry", on_delete=CASCADE, related_name="images")
    image = ForeignKey("wagtailimages.Image", on_delete=CASCADE, related_name="+")

    panels = [
        FieldPanel("image"),
    ]
