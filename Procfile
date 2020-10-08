release: python3 manage.py collectstatic --no-input
release: python3 manage.py migrate
web: gunicorn test_backend.wsgi:application --port $PORT --bind 0.0.0.0