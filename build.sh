#!/usr/bin/env bash
set -o errexit

echo "Installing packages..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Fixing Site..."
python manage.py shell <<EOF
from django.contrib.sites.models import Site
try:
    site = Site.objects.get(id=1)
    site.domain = 'realtime-chat-r818.onrender.com'
    site.name = 'Real-Time Chat'
    site.save()
    print("✅ Site updated")
except Site.DoesNotExist:
    Site.objects.create(id=1, domain='realtime-chat-r818.onrender.com', name='Real-Time Chat')
    print("✅ Site created")
EOF

echo "✅ Build complete!"