#!/bin/sh

python manage.py makemigrations
python manage.py migrate --fake-initial
python manage.py collectstatic --no-input
python manage.py superuser_from_env
exec python manage.py runserver 0.0.0.0:8000