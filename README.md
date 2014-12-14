somejam-2015
============


## General
Remake of the old version, that worked with Google app-engine. This version is now using Heroku, since django deployment seems to be easier.

The old version can be found from branch 'release/somejam-2014-google-appengine'

Buzzwords: heroku, docker, django, python, bootstrap, jquery

## Deployed version

For now its running at http://enigmatic-harbor-4948.herokuapp.com/

It does scheduled (for every 30min):
* Pull JSON feeds for each registered calendar from nusuvefo website

The configuration is done with heroku-config -- that is all secrets are stored as enviroment variables inside the heroku.

## Development

There is docker-file deployed on the root folder. Building should be easy as

> docker build nettiapuanyt

That gives you image. There is no sources included, so make sure to mount it, say with (on the root source folder):

> docker run -v $(pwd)/:/var/www/ -p 5000:5000 -i -t --name NETTIAPU nettiapua:dev /bin/bash

