from apps.base.models import AbstractPageHome, AbstractDetailPage


class IndustryHome(AbstractPageHome):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    subpage_types = ["Industry"]


    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

class Industry(AbstractDetailPage):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    parent_page_types = ["IndustryHome"]
    subpage_types = []

    def get_template(self, request, *args, **kwargs):
        return "industry/industry_page.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)
