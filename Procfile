web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn aiverse_api.wsgi:application --bind 0.0.0.0:$PORT
