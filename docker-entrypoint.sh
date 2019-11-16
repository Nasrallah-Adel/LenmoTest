#!/bin/sh -e

cd $APP_PATH

# check if the database is ready
echo "Waiting for Postgres DB"
sleep 10

echo "Postgres DB is ready"

echo "Collect statics"
./manage.py collectstatic --no-input
# create tables
echo "Updating Database Tables"
./manage.py makemigrations
./manage.py migrate
echo "The Database has been updated"
echo "Creating superuser"
./manage.py initadmin
# run the server
echo "Starting the server..."

gunicorn --bind unix:/run/lenmo.sock LenmoTest.wsgi --reload --access-logfile "/var/access.log" --log-level "debug"