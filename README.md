# todo_test
Simple REST-service for working with the “to-do list”.
The project uses postgresql, django, django rest framework, swagger/redoc auto docs, gunicorn, etc.

# To deploy this project, complete the following steps:

## 1. Development environment configuration
Create from template and modify `.env` file
```bash
cp .env.example .env
```
Set the `SERVER` variable to one of two `dev` or `production` values.  
Set the `SYSTEM_USER` variable for your user (run `id -u && id -g`).

## 2. Docker part
To build `backend` container and run all containers
```bash
docker-compose up -d --build
```

## 3. Run migrations
```bash
docker exec -it backend python manage.py migrate
```

## 4. Load users data to db
```bash
docker exec -it backend python manage.py load_users_to_db
```
Default password for all users is `VerySecurityPassword123`.

## 5. Load tasks data to db
```bash
docker exec -it backend python manage.py load_tasks_to_db
```

## 6. Create superuser for access to admin panel
```bash
docker exec -it backend python manage.py createsuperuser
```

## 7.1 if SERVER == 'production'
If you choose production server you need to collect static.
```bash
docker exec -it -u 0 backend python manage.py collectstatic
```
The production server is served by a gunicorn.  
The number of gunicorn workers and the wsgi port can be set in the env file.  

## 7.2 if SERVER == 'dev'
The development server is served by a runserver.
You can use it directly http://localhost:wsgi_port/ (`wsgi_port` is set in the env file, default is 8000)
or through nginx (http://localhost/).  

In `dev` state you can use auto docs.  
To get into `redoc`, follow the link http://localhost:8000/redoc/  
To get into `swagger`, follow the link http://localhost:8000/swagger/  
To enter the `swagger` rest-client, you need get the access token from http://localhost:8000/auth/ API point,  
then click the `Authorize` button and insert the access token by adding the auth header type "Bearer ".  
For example final string looks like: `Bearer eyJ0eXAiOi...truncated_token...rP9muTz1p9raw1Y`.

## Tests

### Run tests with coverage
```bash
docker exec -it backend coverage run --source='apps/' manage.py test apps.users.tests apps.tasks.tests
```

### Generate report
```bash
docker exec -it backend coverage report
```

### Run flake8 checking
```bash
docker exec -it backend flake8
```
