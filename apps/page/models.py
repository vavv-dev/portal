from apps.base.models import AbstractPageHome, AbstractDetailPage


class PageHome(AbstractPageHome):
    class Meta:
        verbose_name = "페이지"
        verbose_name_plural = verbose_name

    subpage_types = ["Page"]


class Page(AbstractDetailPage):
    class Meta:
        verbose_name = "페이지"
        verbose_name_plural = verbose_name

    parent_page_types = ["PageHome"]
    subpage_types = []

    def get_template(self, request, *args, **kwargs):
        return "page/page.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)
