#!/bin/bash
set -e

echo "migrating DB.."
python manage.py makemigrations api
python manage.py migrate
nohup python manage.py process_tasks --queue=update-managing-queue > back0.out & 
rm package-lock.json
npm install
npm install --save vuetify
echo "run django gunicorn server.."
# gunicorn --bind 0.0.0.0:80 --timeout 3600000 --workers=$(($(getconf _NPROCESSORS_ONLN)*3/2 + 1)) backend.wsgi:application
python manage.py runserver 0:80