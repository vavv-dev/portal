from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import CASCADE, ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        page = request.GET.get("page")
        per_page = request.GET.get("per_page")
        newspages = self.pagination_wrap(self.get_children().live().order_by("-id"), page, per_page or 7)
        context["newspages"] = newspages
        return context

    # TODO // Pagination "더보기"
    def pagination_wrap(self, objs, page, per_page):
        paginator = Paginator(objs, per_page)
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)

        setattr(
            paginator,
            "elided_page_range",
            paginator.get_elided_page_range(
                objs.number,
                on_each_side=3,
                on_ends=1,
            ),
        )

        # numbering
        setattr(
            paginator,
            "base_no",
            (paginator.count or 0) - int(per_page) * (objs.number - 1) - len(objs.object_list),
        )
        return objs

    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)


class News(AbstractDetailPage):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    parent_page_types = ["NewsHome"]
    subpage_types = []

    content_panels = AbstractDetailPage.content_panels + [
        InlinePanel("images", label="이미지"),
    ]

    def get_template(self, request, *args, **kwargs):
        return "news/news_page.html"

    def get_landing_page_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

    def main_image(self):
        gallery_item = self.images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


class NewsImage(Orderable):
    news = ParentalKey("News", on_delete=CASCADE, related_name="images")
    image = ForeignKey("wagtailimages.Image", on_delete=CASCADE, related_name="+")

    panels = [
        FieldPanel("image"),
    ]
