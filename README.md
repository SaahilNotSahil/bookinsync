# BookInSync
Assignment for MoveInSync Backend Developer role.

## Steps to run:
1. Clone the repository. Make sure you have python3 and pip installed, and that you are in the project directory.
2. Using pip, install the requirements.txt file.
```
pip install -r requirements.txt
```
3. Create the .env file.
```
cd backend
cp .env.example .env
```
4. Generate and add a secret key. You can use the following command to generate a secret key.
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
5. Run the migrations.
```
python manage.py migrate
```
6. Create a superuser.
```
python manage.py createsuperuser
```
7. Run the server.
```
python manage.py runserver
```
8. Open the admin panel at http://127.0.0.1:8000/admin/ and login with the superuser credentials.
9. The web application is available at http://127.0.0.1:8000/ and the API is available at http://127.0.0.1:8000/api/.

## Technologies used:
1. Django
2. Django REST Framework
3. SQLite3
4. HTML
5. CSS
6. JavaScript
