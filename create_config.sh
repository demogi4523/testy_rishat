#!/usr/bin/env bash

touch .env

echo "DJANGO_SUPERUSER_USERNAME=admin" >> .env 
echo "DJANGO_SUPERUSER_PASSWORD=qwerty123" >> .env
echo "DJANGO_SUPERUSER_EMAIL=admin@example.com" >> .env
echo "STRIPE_API_PUBLIC_KEY=pk_test_51MdIvZDSkcDnSDCwnrN0SguM7dTEmY42kOvZpbtZurtweGUMLpsOSGhjhHf4mOhqfRIqAHcycgIACFT67Ky4tBkh003UzySjQ9" >> .env
echo "STRIPE_API_SECRET_KEY=sk_test_51MdIvZDSkcDnSDCw1V0iG3jctm5Ch1OXExg918EIp80gU0k1Ac6LdiF0sYilTRXlbuZETjdZZi7oJEKneiW6LjYJ00u5a7S8ZH" >> .env
echo "DEBUG=False" >> .env

echo 'env fail was created'
