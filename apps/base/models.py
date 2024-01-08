from colorfield.fields import ColorField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    F,
    ForeignKey,
    IntegerField,
    OuterRef,
    SET_NULL,
    TextField,
    URLField,
)
from django.db.models.functions import Cast
from django.forms.widgets import ChoiceWidget
from django.http import HttpResponseRedirect
from django_comments_xtd import get_model as get_comment_model
from django_tables2 import RequestConfig
from hitcount.models import HitCount, HitCountMixin
from hitcount.views import HitCountMixin as HitCountViewMixin
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField
from star_ratings.models import Rating
from taggit.models import ItemBase, TagBase
from treenode.admin import TreeNodeModelAdmin
from treenode.models import TreeNodeModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page, ParentalKey
from wagtail.search.index import AutocompleteField, Indexed, RelatedFields, SearchField
from wagtail.snippets.models import register_snippet

from apps.base.blocks import BannerBlock

from .utils import SubqueryCount, random_color


XtdComment = get_comment_model()


@register_snippet
class Tag(TagBase):
    """Tag."""

    class Meta:
        """Meta."""

        verbose_name = "태그"
        verbose_name_plural = verbose_name
        unique_together = ("name",)

    color = ColorField("태그 컬러", default=random_color, format="hexa")


class TaggedPageItem(ItemBase):
    """TaggedPageItem."""

    content_object = ParentalKey(Page, on_delete=CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_items")


@register_snippet
class Category(Indexed, TreeNodeModel):
    """Category."""

    class Meta:
        """Meta."""

        verbose_name = "카테고리"
        verbose_name_plural = verbose_name
        ordering = ["tn_order"]

    treenode_display_field = "name"

    name = CharField("제목", max_length=50, db_index=True)
    description = TextField("설명", null=True, blank=True)

    search_fields = [
        SearchField("name"),
        AutocompleteField("name"),
    ]

    def clean(self):
        """clean."""
        if self.parent:
            no_cache_qs = self.parent.get_children_queryset()
        else:
            no_cache_qs = self.get_roots_queryset()

        if self.name in no_cache_qs.exclude(pk=self.pk).values_list("name", flat=True):
            raise ValidationError("같은 레벨에 중복된 이름이 있습니다.")

    def breadcrumbs_display(self):
        return " / ".join([b.name for b in super().breadcrumbs])


class AbstractPageHome(Page):
    """AbstractPageHome."""

    class Meta:
        """Meta."""

        abstract = True

    subpage_types = []
    max_count = 1
    show_in_menus_default = True

    # fmt: off

    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, verbose_name="커버")
    short_description = TextField("간략한 설명", null=True, blank=True)
    content = StreamField(
        [
            ("banner", BannerBlock(label="배너", required=False)),
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="내용",
        use_json_field=True,
    )

    # fmt: on

    content_panels = Page.content_panels + [
        FieldPanel("cover"),
        FieldPanel("short_description"),
        FieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        """get_context.

        :param request:
        :param args:
        :param kwargs:
        """
        context = super().get_context(request, *args, **kwargs)

        # all pages
        pages = self.get_children_with_annotation().live().order_by("-priority", f"-id")

        # search
        search = request.GET.get("search")
        if search:
            pages = pages.search(search)

        # django tables
        from .tables import PageTable

        page_table = PageTable(pages)

        # filter, sort, pagination
        RequestConfig(request).configure(page_table)

        context.update(page_table=page_table)
        return context

    def get_children_with_annotation(self):
        """get_children_with_annotation."""
        # if not raise
        subpage_type = self.subpage_type().lower()
        return self.get_children().annotate(
            # priority
            priority=F(f"{subpage_type}__priority"),
            # annotate hits
            hit_count=F(f"{subpage_type}__hit__hits"),
            # annotate ratings
            rating_count=F(f"{subpage_type}__rating__count"),
            # annotate ratings
            comment_count=SubqueryCount(
                XtdComment.objects.filter(
                    content_type=OuterRef("content_type"),
                    object_pk=Cast(OuterRef("pk"), output_field=CharField()),
                )
            ),
            # XtdComment.object_id 가 CharField를 사용하기 때문에 GenericRelation을 사용할 수 없음
            # comment_count=Count(f"{subpage_type}__comments__pk"),
        )

    @classmethod
    def subpage_type(cls):
        return cls.subpage_types[0]

    def get_absolute_url(self):
        """get_absolute_url."""
        return self.full_url

    def get_template(self, request, *args, **kwargs):
        return "base/page_home.html"


class AbstractDetailPage(Page, HitCountMixin):
    """AbstractDetailPage."""

    class Meta:
        """Meta."""

        abstract = True

    parent_page_types = []
    subpage_types = []

    content = StreamField(
        [
            ("banner", BannerBlock(label="배너", required=False)),
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="내용",
        use_json_field=True,
    )
    priority = IntegerField("상단 정렬", default=0)
    external_link = URLField("외부 링크", max_length=254, null=True, blank=True)

    allow_rating = BooleanField("추천 사용하기", default=False)
    allow_comments = BooleanField("댓글 사용하기", default=False)
    categories = ParentalManyToManyField(Category, blank=True, verbose_name="카테고리")

    # genertic relation
    tags = ClusterTaggableManager("태그", through=TaggedPageItem, blank=True)
    hit = GenericRelation(HitCount, object_id_field="object_pk")  # OneToOne
    rating = GenericRelation(Rating)  # OneToOne
    comments = GenericRelation(XtdComment, object_id_field="object_pk")  # ManyToMany

    # search

    search_fields = Page.search_fields + [
        SearchField("content"),
        SearchField("first_published_at"),
        SearchField("last_published_at"),
        RelatedFields("tags", [SearchField("name")]),
        RelatedFields("categories", [SearchField("name")]),
        RelatedFields("owner", [SearchField("username"), SearchField("full_name")]),
    ]

    # panel

    content_panels = Page.content_panels + [
        FieldPanel("content"),
        MultiFieldPanel(
            [
                FieldPanel("priority"),
                FieldPanel("allow_rating"),
                FieldPanel("allow_comments"),
                FieldPanel("external_link"),
                FieldPanel("tags"),
                FieldPanel("categories"),
            ],
            heading="설정",
        ),
    ]

    @property
    def hit_count(self):
        """hit_count."""
        # fix: page preview mode
        return super().hit_count if self.pk else HitCount()

    def serve(self, request, *args, **kwargs):
        """serve.

        :param request:
        :param args:
        :param kwargs:
        """

        # update hit
        hit_count = self.hit.get_for_object(self)
        if hit_count:
            HitCountViewMixin.hit_count(request, hit_count)

        if self.external_link:
            return HttpResponseRedirect(self.external_link)

        return super().serve(request, *args, **kwargs)

    def get_absolute_url(self):
        """get_absolute_url."""
        return self.full_url

    def get_template(self, request, *args, **kwargs) -> str:
        return "base/page_detail.html"


class PageFormField(AbstractFormField):
    page = ParentalKey(Page, on_delete=CASCADE, related_name="form_fields")
    label = CharField(verbose_name="제목", max_length=2000)
    help_text = TextField("설명", max_length=255, blank=True)
