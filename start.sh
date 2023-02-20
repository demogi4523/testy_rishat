# deploy
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput

python manage.py makemigrations products
python manage.py migrate products

python manage.py initial_database_fill

gunicorn stripy.wsgi:application --bind 0.0.0.0:8000