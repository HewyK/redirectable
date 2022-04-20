release: python manage.py migrate
web: gunicorn --chdir ppsite redirectable.wsgi:application