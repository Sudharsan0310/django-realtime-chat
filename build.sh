#!/usr/bin/env bash
set -o errexit

echo "==> Installing packages..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Making migrations..."
python manage.py makemigrations

echo "==> Running migrations..."
python manage.py migrate --run-syncdb

echo "==> Creating default site..."
python manage.py shell -c "
from django.contrib.sites.models import Site
site = Site.objects.get_or_create(id=1, defaults={'domain': 'chat-web-application-11a4.onrender.com', 'name': 'Real-Time Chat'})
print('Site created/updated')
"

echo "==> Build complete!"