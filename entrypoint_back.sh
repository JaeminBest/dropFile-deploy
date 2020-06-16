#!/bin/bash
set -e

echo "migrating DB.."
python manage.py makemigrations api
python manage.py migrate
nohup python manage.py process_tasks --queue=update-managing-queue & 
echo "running local backend django server.."
python manage.py runserver 0:2300