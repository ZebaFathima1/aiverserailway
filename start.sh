#!/bin/bash
echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
gunicorn aiverse_api.wsgi:application --bind 0.0.0.0:$PORT
