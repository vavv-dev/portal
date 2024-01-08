from apps.base.models import AbstractPageHome, AbstractDetailPage


class BlogHome(AbstractPageHome):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    subpage_types = ["Blog"]


class Blog(AbstractDetailPage):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    parent_page_types = ["BlogHome"]
    subpage_types = []
