from django.db.models import CASCADE, ForeignKey, SET_NULL, SmallIntegerField
from django.db.models.fields import PositiveBigIntegerField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.models import Orderable, ParentalKey
from wagtail.query import CharField

from apps.base.models import AbstractPageHome, AbstractDetailPage
from apps.base.utils import secure_redeem_code
from apps.course.models import Course


class ProgramHome(AbstractPageHome):
    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = verbose_name

    subpage_types = ["Program"]


class Program(AbstractDetailPage):
    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = verbose_name

    parent_page_types = ["ProgramHome"]
    subpage_types = []

    # fmt: off

    sku = CharField("프로그램 코드", max_length=50, default=secure_redeem_code, unique=True)
    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, verbose_name="커버")
    enrollment_days = SmallIntegerField("수강 기간 일 수", default=60)
    price = PositiveBigIntegerField("가격", default=0)

    # fmt: on

    content_panels = AbstractDetailPage.content_panels + [
        MultiFieldPanel(
            [
                MultipleChooserPanel("courses", "course", label="과정 선택"),
                FieldPanel("sku"),
                FieldPanel("cover"),
                FieldPanel("enrollment_days"),
                FieldPanel("price"),
                MultipleChooserPanel("related_programs", "related_program", label="관련 프로그램"),
            ],
            heading="프로그램 설정",
        )
    ]


class ProgramCourse(Orderable):
    program = ParentalKey(Program, on_delete=CASCADE, related_name="courses")
    course = ForeignKey(Course, on_delete=CASCADE, related_name="+")


class RelatedProgram(Orderable):
    program = ParentalKey(Program, on_delete=CASCADE, related_name="related_programs")
    related_program = ForeignKey(Program, on_delete=CASCADE, related_name="+")
