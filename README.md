# django-starter-peter

This is a rich Django starter project suitable for kickstarting a full-fledged Django site that can be deployed to AWS Elastic Beanstalk.

TODO:

* More about what I get from cookiecutter-django
* More about .ebextensions
* More about deploying to AWS

## Derivation

The project is fairly rich in capabilities, because it was created with [cookiecutter-django](http://cookiecutter-django.readthedocs.io), and successfuly deployed to AWS EB, and along the way picked up various useful libraries, packages, and settings.

## Key Details

### cookiecutter-django

* User accounts

### Front-End

* django-bootstrap4
* django-bootstrap-datepicker-plus
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
* My sortable and filterable mixins

### Administration

* [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface)

### REST APIs

* django-rest-framework

### Data Handling

* PostgreSQL
* django-encrypted-model-fields: Support encrypted storage of sensitive model fields
* django-import-export: Import / export model datasets as CSV, Excel

### Security

* SSL notes
* django-cors-headers
* Storing secrets in S3

### Development

* [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io)

### To Be Sorted / Documented

* Celery
* AWS EB config

#### Works, But Not Included

* [django-extensions](https://django-extensions.readthedocs.io/en/latest/): Additional Django management commands
* [django-grapelli](https://grappelliproject.com/): Modern skin for admin, lets you drag/drop, and regroup on the dashboard

### To Be Tried

#### Front-End

* [jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [django-theme-installer](https://github.com/jefcolbi/django-theme-installer)
* FontAwesome
* Bootstrap4 theming
* Django Vue integrations, see [django-webpack-loader](https://github.com/owais/django-webpack-loader)
* [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/): QuerySet-backed autocomplete for form fields

#### Admin Interface

* [django-admin-tools](https://django-admin-tools.readthedocs.io/): Customize dashboard and menubar

#### Other

* django-imagekit
* from restframework import routers / router = routers.DefaultRouter()
* django-filter (filter down a queryset based on user-supplied parameters)
* [sorl-thumbnail](https://github.com/jazzband/sorl-thumbnail)
* [django-hijack](https://github.com/arteria/django-hijack): Let an admin impersonate a user
* [confidential](https://github.com/candidco/confidential): Store secrets in AWS Secrets Manager
