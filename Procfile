release: python manage.py migrate
worker: celery -A planeks_test worker -l info
web: gunicorn profile_django.wsgi --log-file=-