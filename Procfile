# Procfile
release: python manage.py migrate --noinput
web: gunicorn college_club_management.wsgi:application