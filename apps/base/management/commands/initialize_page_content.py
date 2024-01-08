import logging

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from wagtail.models import Page, Site


log = logging.getLogger("__name__")


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def create_page(self, model_string, title, parent):
        app_label, model_name = model_string.split(".", 1)
        ModelClass = apps.get_model(app_label, model_name)

        try:
            return ModelClass.objects.get(slug=app_label)
        except ModelClass.DoesNotExist:
            pass

        instance = ModelClass(title=title, slug=app_label)
        parent.add_child(instance=instance)

        instance.save()
        instance.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f"{model_string} created"))

        return instance

    def create_portals(self):
        root = Page.get_first_root_node()
        if not root:
            raise ValueError("Root node not exists")

        # create portal page
        portal_model_string, portal_title = settings.BASE_PORTAL
        portal_page = self.create_page(portal_model_string, portal_title, root)
        if not portal_page:
            return

        # create portal sites
        portal_app_label = portal_model_string.split(".")[0]

        try:
            Site.objects.create(
                hostname=f"{portal_app_label}.{settings.BASE_DOMAIN}",
                site_name=portal_title,
                port=settings.PORT,
                is_default_site=False,
                root_page=portal_page,
            )
        except IntegrityError:
            pass

        # create home pages
        if portal_app_label == "portal":
            for page_home_model_string, page_home_title in settings.PAGE_CONTENT:
                # create home pages
                self.create_page(page_home_model_string, page_home_title, portal_page)

        self.stdout.write(self.style.SUCCESS("creating portals done!"))

    def handle(self, *args, **options):
        self.create_portals()
