
#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input

python manage.py migrate
python manage.py createsuperuser --noinput

python manage.py makemigrations products
python manage.py migrate tg_news

python manage.py initial_database_fill