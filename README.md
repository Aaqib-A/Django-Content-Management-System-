# Django-Content-Management-System-


# To Initialize this project
```
django-admin startproject django_cms .
virtualenv -p python3 cms-env
```

# To install this project:
```
source cms-env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# Add Application for Authentication
1. Client type: Confidential
2. Authorization grant type: Resource owner password-based
3. Set user = admin
4. Copy "client_id" and "client_secret" and paste it in postman collection variables
