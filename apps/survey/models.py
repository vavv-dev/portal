from wagtail.admin.panels import InlinePanel
from wagtail.contrib.forms.models import AbstractForm

from apps.base.forms import NormalizedFormBuilder
from apps.base.models import AbstractPageHome, AbstractDetailPage


class SurveyHome(AbstractPageHome):
    class Meta:
        verbose_name = "설문 조사"
        verbose_name_plural = verbose_name

    subpage_types = ["Survey"]

    def get_template(self, request, *args, **kwargs):
        return "survey/survey_home.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

class Survey(AbstractForm, AbstractDetailPage):
    class Meta:
        verbose_name = "설문 조사"
        verbose_name_plural = verbose_name

    form_builder = NormalizedFormBuilder

    parent_page_types = ["SurveyHome"]
    subpage_types = []

    content_panels = AbstractDetailPage.content_panels + [
        InlinePanel("form_fields", label="설문 항목"),
    ]

    def get_template(self, request, *args, **kwargs):
        return "survey/survey.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)
