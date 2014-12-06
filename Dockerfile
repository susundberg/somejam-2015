from ubuntu:14.04
RUN apt-get update
ADD INSTALL /root/INSTALL
RUN apt-get -y --no-install-recommends install wget python-pip
RUN /root/INSTALL/heroku-install-ubuntu.sh


RUN apt-get -y --no-install-recommends install python-django python-psycopg2 python-bs4 gunicorn 

# Not really required but makes debugging easier
RUN apt-get -y --no-install-recommends  install nano 

RUN pip install django-toolbelt

# Make database
RUN /etc/init.d/postgresql start
RUN cp  /root/INSTALL/make-postgress-db.sh /tmp/make-postgress-db.sh
RUN chown postgres: /tmp/make-postgress-db.sh
RUN su --command /tmp/make-postgress-db.sh --shell /bin/bash postgres





