# 4th place Winner: Agilent Technologies Ship-It Hackathon
 
## Instrument-Manager

Instrument Manger is a full-stack web application for visualizing instrument usage and notifying employees once their instrument of interest is available.

## Features
- Django (Back-End)
- Bootstrap 3.x (Front-End)
- RabbitMQ (Broker)
- Celery

## Local Development
## Installation
### 1.	Install Python (3.5.X used), Erlang OTP (21.2), & RabbitMQ (3.7.11) on your machine 

### 2.	Clone the repository
> 'Git clone https://github.com/stbarillas/Instrument-Manager.git'
3.	Running in development mode
a.	In resourceallocationmanager directory:
i.	Activate the virtual environment
ii.	Run python manage.py runserver
iii.	Activate the virtual environment in a separate CMD window
iv.	Run Celery -A mysite worker -l infor
4.	Open the source code and start editing
a.	The sire is now running at http://localhost:8000
b.	Open directory in your code editor of choice and edit it. Save your changes and the browser will update in real time!
## Contact Me
If you have any questions or suggestions please do not hesitate to contact me at stbarillas@gmail.com
