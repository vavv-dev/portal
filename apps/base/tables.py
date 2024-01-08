from itertools import count

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import escape, format_html
from django.utils.html import format_html
from django_tables2 import Column
from django_tables2 import CheckBoxColumn, Column, Table
from wagtail.models import Page


class SelectTableMixin(Table):
    """TableMixin.

    select checkbox column, counter column 추가
    """

    class Meta:
        """Meta."""

        template_name = "django_tables2/bootstrap5.html"
        fields = ()
        default = ""
        attrs = {
            "class": "table",
            "tbody": {"class": "table-group-divider"},
        }
        per_page = 25

    selection = CheckBoxColumn(
        verbose_name="",
        empty_values=(),
        orderable=False,
        exclude_from_export=True,
    )
    counter = Column(
        verbose_name=format_html('<a href=".">NO.</a>'),  # reset sorting
        empty_values=(),
        orderable=False,
        exclude_from_export=True,
    )

    def render_selection(self, value, record):
        """render_selection.

        :param value:
        :param record:
        """
        return format_html(
            f'<input type="checkbox" class="form-check-input" name="selection" value="{record.id}"/>'
        )

    def render_counter(self, value, record):
        """value_counter.

        :param value:
        :param record:
        """
        if not hasattr(self, "page"):
            self.row_counter = getattr(self, "row_counter", count())
            counter = next(self.row_counter) + 1
        else:
            self.row_counter = getattr(self, "row_counter", count())
            counter = next(self.row_counter) + ((self.page.number - 1) * self.paginator.per_page)
            counter = self.page.paginator.count - (counter)

        return counter

    def __init__(self, *args, **kwargs):
        """__init__.

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)


class PageTable(SelectTableMixin):
    class Meta(SelectTableMixin.Meta):
        model = Page

    priority = Column(verbose_name="")
    title = Column(verbose_name="제목")
    last_published_at = Column(verbose_name="수정")
    rating_count = Column(verbose_name="추천")
    hit_count = Column(verbose_name="조회")

    def render_priority(self, value, record):
        return format_html('<i class="fa-regular fa-bell"></i>') if value else ""

    def render_title(self, value, record):
        value = escape(value)
        if record.comment_count:
            value += f" <span>({record.comment_count})</span>"
        return format_html(f'<a href="{record.url}">{value}</a>')

    def render_last_published_at(self, value, record):
        return naturaltime(record.last_published_at)
