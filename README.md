# The PAD

The PAD is a project which aims to create a web server to manage a game with users. Those users will be able to gain and lose points regarding some of their actions.
One other goal is to be able to visualise the points of every user over the time in a graph.

The PAD will be used during parties where each participant will be able to gain and lose points with some games.

This project is also a way to discover django following the tutorial : [django tutorial](https://docs.djangoproject.com/fr/4.0/intro/tutorial01/)


To install all the required packages you have to create a virtual environnement
```
py -m venv ./venv
```
Then you have to activate the venv
```
./venv/Script/activate
```
And lastly you have to install all the packages listed in the file requirement.txt
```
pip install -r .\requirement.txt
```

## Deploy

- In *src/thePAD/settings.py* change **DEBUG** to FALSE
- Make sure that the IP of the machine is in the list `ALLOWED_HOSTS` in settings.py
- launch manage.py like : `python manage.py runserver 0.0.0.0:8000`
- connect to the server with the link [http://192.168.1.24:8000](http://192.168.1.24:8000) (if the ip is 192.168.1.24)