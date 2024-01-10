from django.db.models import (
    CASCADE,
    ForeignKey,
    SET_NULL,
    IntegerField,
    SmallIntegerField,
)
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.models import Orderable, ParentalKey
from wagtail.query import CharField

from apps.base.models import AbstractPageHome, AbstractDetailPage
from apps.base.utils import secure_redeem_code
from apps.course.models import Course


class FlexHome(AbstractPageHome):
    class Meta:
        verbose_name = "플렉스"
        verbose_name_plural = verbose_name

    subpage_types = ["Flex"]


class Flex(AbstractDetailPage):
    class Meta:
        verbose_name = "플렉스"
        verbose_name_plural = verbose_name

    parent_page_types = ["FlexHome"]
    subpage_types = []

    # fmt: off

    number = CharField("플렉스 코드", max_length=50, default=secure_redeem_code, unique=True)
    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, verbose_name="커버")
    enrollment_days = SmallIntegerField("수강 기간 일 수", default=180)

    classification = CharField("분류", max_length=50, default="skill", choices=(("common", "공통역량"), ("leadership", "리더십"), ("skill", "직무역량")))
    leanring_type = CharField("콘텐츠 유형", max_length=50, default="elearning", choices=(("elearning", "이러닝"), ("microlearning", "마이크로러닝"), ("shortform", "숏폼")))
    training_minutes = IntegerField("학습 시간 분", default=0)

    # fmt: on

    content_panels = AbstractDetailPage.content_panels + [
        MultiFieldPanel(
            [
                MultipleChooserPanel("courses", "course", label="과정 선택"),
                FieldPanel("number"),
                FieldPanel("cover"),
                FieldPanel("enrollment_days"),
                FieldPanel("classification"),
                FieldPanel("leanring_type"),
                FieldPanel("training_minutes"),
                MultipleChooserPanel("related_flexes", "related_flex", label="관련 플렉스"),
            ],
            heading="플렉스 설정",
        )
    ]


class FlexCourse(Orderable):
    flex = ParentalKey(Flex, on_delete=CASCADE, related_name="courses")
    course = ForeignKey(Course, on_delete=CASCADE, related_name="+")


class RelatedFlex(Orderable):
    flex = ParentalKey(Flex, on_delete=CASCADE, related_name="related_flexes")
    related_flex = ForeignKey(Flex, on_delete=CASCADE, related_name="+")
