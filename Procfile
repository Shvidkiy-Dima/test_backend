release: python3 manage.py collectstatic --no-input
release: python3 manage.py migrate
release: python3 manage.py superuser_from_env
web: gunicorn test_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: exec celery -A test_backend worker -B