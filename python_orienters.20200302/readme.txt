Brief
-----
These are setup instructions for the echo
portion of Python Orienters.

It also includes the identifier, illuminator,
connector & reflector modules which were completed
earlier.




Setup
-----
The following may not work on all machines
due to software incompatibilities etc.

The instructions were based on setting up the web app on
an Ubuntu Linux variant operating system called Pop OS!

The instructions assumed you already followed the steps
outlined in an earlier readme.txt for the **identifier**
portion of the project.



1) Assuming your home directory is at /home/ian,
and /home/ian/Documents exists, remove the earlier
identifier files by deleting these directories:

/home/ian/Documents/python_orienters/django/dreamit/dreamit
/home/ian/Documents/python_orienters/django/dreamit/orienters

2) Delete all files in this directory except "placeholder.jpg"

/home/ian/Documents/python_orienters/django/dreamit/orienters/static/tmp

3) Extract the zip and copy its contents (overwriting existing files),
such that you will have these directories afterwards:

/home/ian/Documents/python_orienters/django/dreamit/dreamit
/home/ian/Documents/python_orienters/django/dreamit/orienters
/home/ian/Documents/python_orienters/sql

4) Activate the virtual environment & install some packages:

cd /home/ian/Documents/python_orienters
source ./django/bin/activate
cd django/dreamit
pip3 install requests

5) Run Django migration to update the database:

cd django/dreamit
python3 manage.py migrate

6) Execute /home/pmg/Documents/python_orienters/sql/dreamit.sql onto database 'dreamit'.

mysql -u dreamit -D dreamit -p
> source /home/pmg/Documents/python_orienters/sql/dreamit.sql;
> show tables;

7) Run the server:

cd /home/ian/Documents/python_orienters/django/dreamit
python3 manage.py runserver

8) You can now see the web app at http://localhost:8000/orienters/login
See the section 'Django users' below for login credentials you can use

9) To shut down the server, press CTRL+C on the console it runs on,
then type:
deactivate




Managing Django groups & users
------------------------------
# To manage groups, go to http://localhost:8000/admin/auth/group/

# To manage users (and the group(s) they belong to), go to http://localhost:8000/admin/auth/user/

# The admin/superuser account was created using command line : python manage.py createsuperuser
[description : username/password]
superuser : pmg/s+uPC@V+7p

# These users were added using page : http://localhost:8000/admin/auth/user/add/
[description : username/password]
male user : joe/4kAqX%VTeG8t
female user : jill/RAk8m$k@PF
female user with no identifier or illuminator reports : jaqo/s3x*QG}d/b
