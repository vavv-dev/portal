from apps.base.models import AbstractPageHome, AbstractDetailPage


class EventHome(AbstractPageHome):
    class Meta:
        verbose_name = "이벤트"
        verbose_name_plural = verbose_name

    subpage_types = ["Event"]


class Event(AbstractDetailPage):
    class Meta:
        verbose_name = "이벤트"
        verbose_name_plural = verbose_name

    parent_page_types = ["EventHome"]
    subpage_types = []
