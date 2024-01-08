import random
import re
import secrets
import string
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import IntegerField, Subquery


def random_color():
    """random_color."""
    rand = lambda: random.randint(100, 255)
    return "#%02X%02X%02X" % (rand(), rand(), rand())


def secure_redeem_code(length=8):
    characters = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(characters) for _ in range(length))
    return code


def random_four_digit():
    return str(random.randint(1000, 9999))


def upload_unique_name(instance, filename, *args, **kwargs):
    class_name = instance.__class__.__name__
    dirname = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
    return "{0}/{2}.{1}.{3}".format(dirname, uuid4().hex[:8], *filename.rsplit(".", 1))


def validate_esimsa_code(value: str):
    pattern = re.compile(r"^\w\d{8}\d{4}\w\d\d\d{2}\d{2}$")
    if not pattern.match(value):
        raise ValidationError("코드 형식이 올바르지 않습니다.")


def paginate(objs, page, per_page):
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
        paginator.get_elided_page_range(objs.number, on_each_side=3, on_ends=1),
    )

    # numbering
    setattr(
        paginator,
        "base_no",
        (paginator.count or 0) - int(per_page) * (objs.number - 1) - len(objs.object_list),
    )
    return objs


class SubqueryCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()
