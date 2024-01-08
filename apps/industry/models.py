from apps.base.models import AbstractPageHome, AbstractDetailPage


class IndustryHome(AbstractPageHome):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    subpage_types = ["Industry"]


class Industry(AbstractDetailPage):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    parent_page_types = ["IndustryHome"]
    subpage_types = []
