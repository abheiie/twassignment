# Django Application over StackOverflowAPI for searching questions

## Functionality requirement
1) Should be able to search all available fields/parameters. 
2) List the result with pagination with Django template (Using Restful API and angular/react bonus).
3) Page/Data should be cached. (Application should only call StackOverflowAPI if we didn't pull data already for same query param)
4) Add Search limit per min(5) and per day(100) for each session.

## Technology used
1) [Memcached](https://memcached.org/) for caching purpose
2) Python
3) Django
3) Bootstrap
4) HTML
5) Sqlite

## Resource used
1) StackOverflowAPI


## Setup
### Setup Memcached
1) The first thing to do is install and configure "Memcached", make sure it runs on its default port - "11211"

```sh
https://crunchify.com/install-setup-memcached-mac-os-x/
```

2) Configuring Memcached for Django project (this part is done already in project)

```sh
https://micropyramid.com/blog/python-memcached-implementation-for-django-project/
```

### Setup Django Project
1) Create and activate python virtual environment
```sh
$ python3 -m venv env
$ source env/bin/activate
```
2) Clone the project
```sh
$ git clone https://github.com/ramsey009/twassignment.git
$ cd twassignment
```

3) Install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
4) Migrate the database
```sh
(env)$ python manage.py migrate
```
5) Run Server (make sure Memcached server is running already)
```sh
(env)$ python manage.py runserver
```