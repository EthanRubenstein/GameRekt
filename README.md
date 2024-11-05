# GameRekt: Social Videogame Database

## Active proof of concept link: http://ec2-3-128-155-155.us-east-2.compute.amazonaws.com/

## Startup instructions


make sure you have python and run pip install -r requirements.txt

run:
```
set FLASK_APP=app.py
set FLASK_ENV=development
py -m flask run
```
init database with: py -m flask initdb (currently does nothing)

To-do list:
-Profile pictures
-Pagination of search results
-More advanced query system to account for mispellings, stem shortening, etc
-Messaging system
-Notification system
-Settings page
