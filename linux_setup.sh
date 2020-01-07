#!/bin/bash

# get python
sudo apt-get install python3.7

sudo apt-get update

# get django
sudo pip install django

# make migrations
python manage.py makemigrations

# migrate
python manage.py migrate