#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create Site with ID=2 for chat
python manage.py shell <<EOF
from django.contrib.sites.models import Site
try:
    site = Site.objects.get(id=2)
    site.domain = 'chat-web-application-11a4.onrender.com'
    site.name = 'Real-Time Chat'
    site.save()
    print("✅ Site ID 2 updated")
except Site.DoesNotExist:
    Site.objects.create(
        id=2,
        domain='chat-web-application-11a4.onrender.com',
        name='Real-Time Chat'
    )
    print("✅ Site ID 2 created")
EOF