from datetime import datetime
import random
import string

from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
    TextField,
    URLField,
)
from django.forms import Field
from django.utils.timezone import make_aware
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search.index import SearchField

from apps.base.models import AbstractPageHome, AbstractDetailPage
from apps.base.utils import validate_esimsa_code

from .blocks import TextbookBlock, TuitionAssistanceBlock, TutorBlock


def random_number():
    return Course.random_number()


class CourseHome(AbstractPageHome):
    class Meta:
        verbose_name = "과정"
        verbose_name_plural = verbose_name

    subpage_types = ["Course"]


class Course(AbstractDetailPage):
    class Meta:
        verbose_name = "과정"
        verbose_name_plural = verbose_name

    parent_page_types = ["CourseHome"]
    subpage_types = []

    # fmt: off

    number = CharField("과정 코드", max_length=50, default=random_number, unique=True)
    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, verbose_name="커버")
    description = TextField("잛은 설명", null=True, blank=True)
    target = TextField("대상", null=True, blank=True)
    objective = TextField("학습목표", null=True, blank=True)
    grading = TextField("평가 방법", null=True, blank=True)
    created_date = DateField("출시 날짜", null=True, blank=True)
    preview = URLField("미리보기", null=True, blank=True)
    contents = TextField("목차", null=True, blank=True)
    effort = CharField("학습 시간", max_length=20, null=True, blank=True)
    level = CharField("레벨", max_length=20, null=True, blank=True)
    ncs_unit = ForeignKey("ncs.NcsClassification", on_delete=SET_NULL, null=True, blank=True, verbose_name="NCS 분류")
    mobile = BooleanField("모바일", default=True)

    tuition_assistances = StreamField(
        [("tuition_assistance", TuitionAssistanceBlock())],
        null=True,
        blank=True,
        verbose_name="교육비 지원",
        use_json_field=True
    )
    tutors = StreamField(
        [("tutor", TutorBlock())],
        null=True,
        blank=True,
        verbose_name="교강사",
        use_json_field=True
    )
    textbooks = StreamField(
        [("textbook", TextbookBlock())],
        null=True,
        blank=True,
        verbose_name="교재",
        use_json_field=True,
    )

    esimsa_code = CharField("esimsa 코드", max_length=50, null=True, blank=True, validators=[validate_esimsa_code])
    esimsa_code_expiration = DateTimeField("과정 승인 만료", null=True, blank=True)
    hrdnet_code = CharField("hrdnet 코드", max_length=50, null=True, blank=True)

    # fmt: on

    content_panels = AbstractDetailPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("number"),
                FieldPanel("cover"),
                FieldPanel("description"),
                FieldPanel("target"),
                FieldPanel("objective"),
                FieldPanel("grading"),
                FieldPanel("created_date"),
                FieldPanel("preview"),
                FieldPanel("contents"),
                FieldPanel("effort"),
                FieldPanel("level"),
                FieldPanel("ncs_unit"),
                FieldPanel("mobile"),
                FieldPanel("tuition_assistances"),
                FieldPanel("tutors"),
                FieldPanel("textbooks"),
                FieldPanel("esimsa_code"),
                FieldPanel("esimsa_code_expiration"),
                FieldPanel("hrdnet_code"),
            ],
            heading="과정 정보",
        )
    ]

    @classmethod
    def random_number(cls):
        number = None
        while True:
            number = "".join(random.choices(string.ascii_lowercase, k=8))
            if not cls.objects.filter(number=number).exists():
                break
        return number

    @property
    def training_type(self):
        """훈련 유형"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[0:1].upper()

        if code == "I":
            return "인터넷원격"
        elif code == "P":
            return "우편원격"
        elif code == "U":
            return "기업대학"
        elif code == "C":
            return "콘소시엄"
        elif code == "H":
            return "스마트훈련"
        elif code == "B":
            return "혼합훈련"
        elif code == "N":
            return "실업자원격"
        elif code == "D":
            return "디지털융합"

    @property
    def content_start_date(self):
        """심사 발급 일자"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[1:9]

        try:
            return make_aware(datetime.strptime(code, "%Y%m%d"))
        except:
            return None

    @property
    def is_postal_course(self):
        """우편 과정"""
        return True if self.training_type == "P" else False

    @property
    def content_category(self):
        """심사 유형"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[13:14]

        if code == "L":
            return "전문직무"
        elif code == "F":
            return "외국어"
        elif code == "A":
            return "NCS 적용 과정"
        elif code == "R":
            return "법정직무과정"
        elif code == "C":
            return "공통법정"
        elif code == "D":
            return "직무법정"
        elif code == "J":
            return "공통직무"

    @property
    def supply_level(self):
        """공급 정도"""

        if not self.esimsa_code:
            return

        level = self.esimsa_code.replace("-", "")[14:15]

        if level == "1":
            return 0.7
        elif level == "2":
            return 0.8
        elif level == "3":
            return 0.9
        elif level == "4":
            return 1.0

    @property
    def content_grade(self):
        """과정 코드 심사 등급"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[15:16]

        if code == "1":
            return "A등급"
        elif code == "2":
            return "B등급"
        elif code == "3":
            return "C등급"
        else:
            return

    @property
    def training_hours(self):
        """훈련 시간"""

        if not self.esimsa_code:
            return

        return self.esimsa_code.replace("-", "")[16:18]
