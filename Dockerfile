from ubuntu:14.04
RUN apt-get update
RUN apt-get -y --no-install-recommends install wget python-pip

RUN apt-get -y --no-install-recommends install python-django python-bs4 python-dateutil python-tz

# I guess we could also use sqlite for local development and skip the gunicorn, but this way its closer
# to deployment enviroment
RUN apt-get -y --no-install-recommends install python-psycopg2 gunicorn
RUN apt-get -y --no-install-recommends install postgresql

# Make database
ADD INSTALL /root/INSTALL
RUN cp  /root/INSTALL/make-postgress-db.sh /tmp/make-postgress-db.sh
RUN chown postgres: /tmp/make-postgress-db.sh
RUN su --command /tmp/make-postgress-db.sh --shell /bin/bash postgres

# Not really required but makes debugging easier
RUN apt-get -y --no-install-recommends install nano ipython

RUN /root/INSTALL/heroku-install-ubuntu.sh
RUN pip install django-toolbelt





