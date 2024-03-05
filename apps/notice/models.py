from apps.base.models import AbstractPageHome, AbstractDetailPage


class NoticeHome(AbstractPageHome):
    class Meta:
        verbose_name = "게시판"
        verbose_name_plural = verbose_name

    subpage_types = ["Notice"]

    def get_template(self, request, *args, **kwargs):
        return "notice/notice_home.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        noticepages = self.get_children().live().order_by("-id")
        context["noticepages"] = noticepages
        return context


class Notice(AbstractDetailPage):
    class Meta:
        verbose_name = "게시판"
        verbose_name_plural = verbose_name

    parent_page_types = ["NoticeHome"]
    subpage_types = []

    def get_template(self, request, *args, **kwargs):
        return "notice/notice_detail.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

    def get_parent(self, update=False):
        return NoticeHome.objects.first()
