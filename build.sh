#!/usr/bin/env bash
set -o errexit

echo "Installing packages..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Setting up Site ID 2 for chat..."
python manage.py shell <<EOF
from django.contrib.sites.models import Site

# Check if Site ID 2 exists
try:
    site = Site.objects.get(id=2)
    site.domain = 'realtime-chat-r818.onrender.com'
    site.name = 'Real-Time Chat'
    site.save()
    print("✅ Site ID 2 updated")
except Site.DoesNotExist:
    # Create Site ID 2 for chat project
    Site.objects.create(
        id=2,
        domain='realtime-chat-r818.onrender.com',
        name='Real-Time Chat'
    )
    print("✅ Site ID 2 created")

# Show all sites
print("
All sites in database:")
for site in Site.objects.all():
    print(f"  - Site {site.id}: {site.domain} ({site.name})")
EOF

echo "✅ Build complete!"