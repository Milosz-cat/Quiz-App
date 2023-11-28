# Django Quiz App

Simple quiz-app built with Django.

## Features

- ELK for monitoring
- CRUD functionality with quizzes and questions
- validation of new quizzes/questions by sending email to admins if the user does not have admin status
- password reset by sending an email with a link
- user authentication system
- template-based interface styled with bootstrap
- after the quiz is finished, a summary of the table of top 5 results based on points and time is displayed

## 🛠 Skills
<p align="left">  
    <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python"             width="40" height="40"/> </a>
    <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> 
    <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg"         alt="docker" width="40" height="40"/> </a>  
    <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg"         alt="bootstrap" width="40" height="40"/> </a>
    <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg"              alt="html5" width="40" height="40"/> </a>
    <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg"         alt="css3" width="40" height="40"/> </a>
</p>

## Preview

![App Screenshot](https://github.com/Milosz-cat/Quiz-App/blob/main/screenshots/Screenshot%20from%202023-03-11%2015-59-48.png)

![App Screenshot](https://github.com/Milosz-cat/Quiz-App/blob/main/screenshots/Screenshot%20from%202023-03-11%2016-01-09.png)

![App Screenshot](https://github.com/Milosz-cat/Quiz-App/blob/main/screenshots/Screenshot%20from%202023-03-11%2016-02-23.png)

## Requirements
* docker and docker compose
* python>=3.10

## Installation

To get this repository, run the following command inside your terminal:

```bash
git clone https://github.com/Milosz-cat/Quiz-App.git
```

Next, create an `.env` file where the `docker-compose.yml` is and copy an fill the content from the `.env.sample` file:
```
cp .env.sample .env
```
For sending e-mails to work properly on your gamil, you need to go to settings and enable two-step verification and then set a password for the application. Here is helpful  [link.](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab)

If you encounter any problem while trying to key access to tmdb API or functionality to send e-mails write to me and I will share my personal data with you. [![email badge](https://img.shields.io/badge/miloszbochenek20@gmail.com-red?style=flat&logo=gmail&logoColor=white&labelColor=red)](mailto:miloszbochenek20@gmail.com)  


Example:
```env
EMAIL_HOST_USER="enter_your_email@gmail.com
EMAIL_HOST_PASSWORD="your_app_password
```

In the same directory, where the `docker-compose.yml` is, run the following commands:
```
docker compose build
```
## Usage

To start the container and test the api run the following command:
```
docker compose up
```

Now you can head over to http://0.0.0.0:8000 to test the app.


To stop the container run:
```
docker compose down
```

You can create admin account (LOGIN=admin, PASSWORD=admin):
```
docker-compose run --rm -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com app python manage.py createsuperuser --no-input
```

Or if you want create your own admin:
```
docker compose run --rm app python manage.py createsuperuser
```
