
#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input

python manage.py migrate
python manage.py createsuperuser --noinput

python manage.py makemigrations products
python manage.py migrate products

python manage.py makemigrations custom_auth
python manage.py migrate custom_auth

python manage.py initial_database_fill
# python manage.py add_stripe_webhook
