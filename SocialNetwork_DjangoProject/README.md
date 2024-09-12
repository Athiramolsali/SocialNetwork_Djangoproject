
# Django Social Networking API

This project uses Django and the Django Rest Framework to create a social networking API. It has features for friend request management, sending and receiving friend requests, user authentication, and rate-limiting friend requests.

## Features

- **User Signup and Login**: Users have the capability to register using an email and password and subsequently log in using their chosen credentials.
- **User Search**: Search for users by name or email with pagination support.
- **Friend Request Management**: Users can initiate, accept, or decline friend requests.
- **Rate Limiting**: Users are restricted to sending a maximum of 3 friend requests per minute.


### Prerequisites

- Python 3.x
- Django 3.x or 4.x
- Django Rest Framework
- SQLite (default) or any database of choice
- pip (Python package manager)
#### Python And Django Setup
Required Python Version: Python 3.10.X

1. Move to project folder  
    `cd ./social_network`
2. Install required python packages  
    `pip install -r requirements.txt`
3. Create database migrations in django  
    `python manage.py makemigrations `
4. Write migration changes in database  
    `python manage.py migrate `
   - In case of 'ProgrammingError': relation `<table-name>` already exists, run  
        `python manage.py migrate --fake-initial `
5.  Create superuser  
    `python manage.py createsuperuser `
6.  Run Django server  
    `python manage.py runserver 0.0.0.0:8000 `



## Misc Python Notes
### How to run scripts with Django shell
1. Starting Django shell  
    `python manage.py shell `  
2. Run an external script in the shell  
    `exec(open('scripts/filename.py').read())`
## How to delete all django database migration files
`find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`  
`find . -path "*/migrations/*.pyc"  -delete`  



#Docker Setup 
1. `Build the Docker Image`
2.`Run the Docker Container`
3.`Run Database Migrations in Docker`
 

