from django.db.models import CharField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm

from apps.base.forms import NormalizedFormBuilder
from apps.base.models import AbstractPageHome, AbstractDetailPage


class SubmitHome(AbstractPageHome):
    class Meta:
        verbose_name = "양식"
        verbose_name_plural = verbose_name

    subpage_types = ["Submit"]


class Submit(AbstractEmailForm, AbstractDetailPage):
    class Meta:
        verbose_name = "양식"
        verbose_name_plural = verbose_name

    form_builder = NormalizedFormBuilder

    parent_page_types = ["SubmitHome"]
    subpage_types = []

    # field override
    subject = CharField("이메일 제목", max_length=255, blank=True)

    content_panels = AbstractDetailPage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("to_address"), FieldPanel("subject")],
            "이메일 전달",
        ),
        InlinePanel("form_fields", label="제출 항목"),
    ]

    def get_template(self, request, *args, **kwargs):
        return "submit/submit.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)
