from django.db.models import CharField, Model
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet


@register_snippet
class NcsClassification(Indexed, Model):
    class Meta:
        verbose_name = "ncs 분류"
        verbose_name_plural = verbose_name

    id = CharField("분류 코드", max_length=10, primary_key=True)
    class1_code = CharField("대분류 코드", max_length=10)
    class1_name = CharField("대분류 명칭", max_length=100, db_index=True)
    class2_code = CharField("중분류 코드", max_length=10)
    class2_name = CharField("중분류 명칭", max_length=100, db_index=True)
    class3_code = CharField("소분류 코드", max_length=10)
    class3_name = CharField("소분류 명칭", max_length=100, db_index=True)

    search_fields = [
        SearchField("id"),
        SearchField("class1_name"),
        SearchField("class2_name"),
        SearchField("class3_name"),
        AutocompleteField("id"),
        AutocompleteField("class1_name"),
        AutocompleteField("class2_name"),
        AutocompleteField("class3_name"),
    ]

    def __str__(self) -> str:
        return f"{self.id} / {self.class1_name} / {self.class2_name} / {self.class3_name}"
