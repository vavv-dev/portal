from apps.base.models import AbstractPageHome, AbstractDetailPage


class NoticeHome(AbstractPageHome):
    class Meta:
        verbose_name = "게시판"
        verbose_name_plural = verbose_name

    subpage_types = ["Notice"]


class Notice(AbstractDetailPage):
    class Meta:
        verbose_name = "게시판"
        verbose_name_plural = verbose_name

    parent_page_types = ["NoticeHome"]
    subpage_types = []
