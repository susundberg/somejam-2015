from ubuntu:14.04
RUN apt-get update
ADD INSTALL /root/INSTALL
RUN apt-get -y --no-install-recommends install wget python-pip
RUN /root/INSTALL/heroku-install-ubuntu.sh


RUN apt-get -y --no-install-recommends  install python-django python-psycopg2 gunicorn 
RUN pip install django-toolbelt

RUN apt-get -y --no-install-recommends  install nano
RUN chsh --shell /bin/bash www-data 




