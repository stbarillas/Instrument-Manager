# 🏆 4th place: Agilent Technologies Ship-It Hackathon 🏆
 
## Instrument-Manager
Instrument Manger is a full-stack web application for visualizing instrument usage and notifying employees once their instrument of interest is available.


## Languages and Tools 💻
- Python
- Django (Back-End)
- Javascript
- HTML
- CSS
- Bootstrap 3.x (Front-End)
- RabbitMQ (Broker)
- Celery


## Local Development 💾 💿 🕹
### Installation 
#### 1.	Install Python (3.5.X used), Erlang OTP (21.2), & RabbitMQ (3.7.11) on your machine 


#### 2.	Clone the repository 
> 'Git clone https://github.com/stbarillas/Instrument-Manager.git'


#### 3. SMTP Setup 
In order for notifications to work, you will need an email service. SendGrid SMTP is a free solution I use for development
- Open 'Instrument-Manager\mysite\settings.py with your code editor of choice and enter your SendGrid SMTP settings (~Lines 120-130)


#### 4.	Running in development mode 
In *Instrument-Manager* directory:

Activate the virtual environment
> 'myvenv\Scripts\activate'

Start the Django Server
> 'python manage.py runserver'

Start the Celery worker in a seperate CMD window with virtual environment activated
> 'celery -A mysite worker -l info'


#### 5.	Open the source code and start editing 
The site is now running at
[http://localhost:8000](http://localhost:8000)

Open *Resource-Allocation-Manager* directory in your code editor of choice and edit it. Save your changes and the browser will update in real time!


## Contact Me 📞
If you have any questions or suggestions please do not hesitate to contact me at stbarillas@gmail.com
