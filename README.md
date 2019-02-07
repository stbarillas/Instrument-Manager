# 4th place Winner: Agilent Technologies Ship-It Hackathon
 
## Instrument-Manager

Instrument Manger is a full-stack web application for visualizing instrument usage and notifying employees once their instrument of interest is available.

## Languages and Tools
- Python
- Django (Back-End)
- Javascript
- HTML
- CSS
- Bootstrap 3.x (Front-End)
- RabbitMQ (Broker)
- Celery

## Local Development
### Installation
#### 1.	Install Python (3.5.X used), Erlang OTP (21.2), & RabbitMQ (3.7.11) on your machine 

#### 2.	Clone the repository
> 'Git clone https://github.com/stbarillas/Instrument-Manager.git'

#### 3. SMTP Setup
In order for notifications to work, you will need an email service. SendGrid SMTP is a free solution I use for development
- Open 'Resource-Allocation-Manager\mysite\settings.py with your code editor of choice and enter your SendGrid SMTP settings (~Lines 120-130)

#### 4.	Running in development mode
a.	In Resource-Allocation-Manager directory:
i.	Activate the virtual environment
ii.	Run python manage.py runserver
iii.	Activate the virtual environment in a separate CMD window
iv.	Run Celery -A mysite worker -l infor

#### 5.	Open the source code and start editing
a.	The sire is now running at http://localhost:8000
b.	Open directory in your code editor of choice and edit it. Save your changes and the browser will update in real time!

## Contact Me
If you have any questions or suggestions please do not hesitate to contact me at stbarillas@gmail.com
