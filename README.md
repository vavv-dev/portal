# vavv portal

## 개발 환경

### provisioning

```bash
$ python3.11 -m venv venv
$ source venv/bin/activate
$ make provision
$ python manage.py runserver
```

### 테스트 사이트

- http://localhost:8000/admin
- http://portal.localhost:8000
- superuser: username vavv / password vavv

### 샘플 과정, 프로그램, 카테고리 등록

```bash
$ python manage.py migrate
$ python manage.py loaddata_courses fixtures/course_list.xlsx
```
