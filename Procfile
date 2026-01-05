web: python manage.py collectstatic --noinput ; python manage.py migrate --noinput ; gunicorn aiverse_api.wsgi:application --bind 0.0.0.0:$PORT
