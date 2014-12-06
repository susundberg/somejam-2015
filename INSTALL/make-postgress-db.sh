#!/bin/bash



createdb djangodb

createuser www-data --no-password --createdb 
echo 'GRANT ALL PRIVILEGES ON DATABASE djangodb TO "www-data;"' | psql

