.DEFAULT_GOAL := help

.PHONY: pip.tools pip.compile \
				requirements \
				provision

help:
	@echo "Read Makefile"

PIP_COMPILE = pip-compile --upgrade --no-strip-extras

pip.tools:
	pip install -r requirements/pip.txt

pip.compile: pip.tools
	$(PIP_COMPILE) -o requirements/pip.txt requirements/pip.in
	$(PIP_COMPILE) -o requirements/base.txt requirements/base.in
	$(PIP_COMPILE) -o requirements/test.txt requirements/test.in
	$(PIP_COMPILE) -o requirements/dev.txt requirements/dev.in
	$(PIP_COMPILE) -o requirements/production.txt requirements/production.in

requirements: pip.tools
	pip-sync requirements/dev.txt

provision: requirements
	python manage.py migrate
	python manage.py initialize_page_content
	@echo 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser("vavv", "vavv@example.com", "vavv") if not User.objects.filter(username="vavv").exists() else None' | python manage.py shell
	mkdir -p portal/static

