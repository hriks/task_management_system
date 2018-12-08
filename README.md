# task_management_system
==========================

## Setting up development environment

Make sure you are using virtualenv

The development environment can be setup either like a pythonista
with the usual python module setup.

## How to install?

Ensure that you have an updated version of pip

```
pip --version
```
Should atleast be 1.5.4
To update pip use

```
pip install -U pip
```
This will upgrade pip version to the latest

From the module folder install the dependencies. This also installs
the module itself in a very pythonic way.

```
pip install -r requirements.txt
```

## Migrations
run the following code to migrate
```
python manage.py makemigrations
```

```
python manage.py migrate
```
run the server by using python manage.py runserver

## Note
Redis-server has to be setup before using this project and
Postgresql is also required.
