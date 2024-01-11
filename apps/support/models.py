from django.db import models
from wagtail.models import Page

from apps.notice.models import Notice


# Create your models here.
class SupportHome(Page):
    class Meta:
        verbose_name = "고객센터"
        verbose_name_plural = verbose_name

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["notices"] = Notice.objects.all().live()
        return context
