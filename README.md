# BierApp
Drink management system for student houses. This is the server part.

## Requirements
* Django 1.7
* MySQL database

## Installation
* Install the dependencies.
* Clone this repository.
* Run `python manage.py migrate` to synchronize the database scheme.
* Run `python manage.py createsuperuser` to create an administrator account.
* Run `python manage.py collectstatic` to copy static files to the `static/` folder.

## Todo
There is a lot of work to do to make it a better and more manageable system. Nonetheless, it is a working product that has served 3000+ transactions without problems.

* Better user handling and signup flow
* Create/Edit forms for all objects
* Better UI
* Better Forms

## License
See the `LICENSE` file (GPLv3 license). You may change the code freely, but any change must be made available to the public.

The landing page background images originate from Flickr (Creative Commons, commercial use allowed).