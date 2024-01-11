from apps.base.models import AbstractPageHome, AbstractDetailPage


class NewsHome(AbstractPageHome):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    subpage_types = ["News"]

    def get_template(self, request, *args, **kwargs):
        return "news/news_home.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)


class News(AbstractDetailPage):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    parent_page_types = ["NewsHome"]
    subpage_types = []

    def get_template(self, request, *args, **kwargs):
        return "news/news_page.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)
