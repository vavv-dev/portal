from django.db.models import ForeignKey, SET_NULL
from wagtail.admin.panels import FieldPanel

from apps.base.models import AbstractPageHome, AbstractDetailPage


class PartnerHome(AbstractPageHome):
    class Meta:
        verbose_name = "파트너"
        verbose_name_plural = verbose_name

    subpage_types = ["Partner"]


class Partner(AbstractDetailPage):
    class Meta:
        verbose_name = "파트너"
        verbose_name_plural = verbose_name

    parent_page_types = ["PartnerHome"]
    subpage_types = []

    logo = ForeignKey("wagtailimages.Image", on_delete=SET_NULL, null=True, verbose_name="로고")

    content_panels = AbstractDetailPage.content_panels + [
        FieldPanel("logo"),
    ]
