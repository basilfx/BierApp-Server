# BierApp
Drink management system for student houses. This is the server part.

## Introduction
This projected once started as a complete studen house management system: cooking, finance, tasks and more. The more part included 'apps' that could be used to extend functionality for specific houses. The actual system was never finished, and only the drink management app was used. Since I graduated in 2015, I am not planning to finish the whole system, but my (former) house is still using the drink management app to register consumptions. I decided to remove everything but the BierApp part, and so it began.

The system is not complete, but it works and is usable.

## Screenshots
![Login screen](https://raw.github.com/basilfx/BierApp-Server/master/docs/screenshots/login.png)

![Dashboard](https://raw.github.com/basilfx/BierApp-Server/master/docs/screenshots/dashboard.png)

![Statistics](https://raw.github.com/basilfx/BierApp-Server/master/docs/screenshots/statistics.png)

## Requirements
* Python 3.6
* Django 1.11
* PostgreSQL database
* BierApp client

## Installation
* Install the dependencies using `pip install -r requirements.txt`.
* Clone this repository.
* Run `python manage.py migrate` to synchronize the database scheme.
* Run `python manage.py createsuperuser` to create an administrator account.
* Run `python manage.py bower_install` to install Bower components (requires Bower on your PATH).
* Run `python manage.py collectstatic` to copy static files to the `static/` folder.

## Todo
There is a lot of work to do to make it a better and more manageable system. Nonetheless, it is a working product that has served 3000+ transactions without problems.

* Better user handling and signup flow
* Create/Edit forms for all objects
* Better UI
* Better Forms
* Better API

## License
See the `LICENSE` file (GPLv3 license). You may change the code freely, but any change must be made available to the public.

The landing page background images originate from Flickr (Creative Commons, commercial use allowed).
