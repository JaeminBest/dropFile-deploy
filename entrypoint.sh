#!/bin/bash
set -e

echo "migrating DB.."
python manage.py makemigrations api
python manage.py migrate
# nohup python manage.py process_tasks --queue=update-managing-queue & 
rm -f package-lock.json
echo "running local server django gunicorn server.."
# gunicorn --bind 0.0.0.0:80 -D --timeout 3600000 --workers=$(($(getconf _NPROCESSORS_ONLN)/2 + 1)) backend.wsgi:application  
npm run serve