release: python3 test_backend/manage.py collectstatic --no-input
release: python3 test_backend/manage.py migrate
web: gunicorn test_backend.test_backend.wsgi:application --port $PORT --bind 0.0.0.0