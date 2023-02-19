#!/usr/bin/env bash

if [[ ! -f "./.env" ]];
then
    source create_config.sh
fi

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd stripy

python manage.py migrate
python manage.py createsuperuser --noinput

python manage.py makemigrations products
python manage.py migrate products

python manage.py runserver
