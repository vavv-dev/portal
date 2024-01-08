from apps.base.models import AbstractPageHome, AbstractDetailPage


class NewsHome(AbstractPageHome):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    subpage_types = ["News"]


class News(AbstractDetailPage):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    parent_page_types = ["NewsHome"]
    subpage_types = []
