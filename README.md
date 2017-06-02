# Attendance Portal
-------------------

## Set up the project
##### For Ubuntu and Debian-based systems

Clone the repo
```git clone https://github.com/Symphoria/attendance-portal.git```

Go into the project directory
```cd attendance-portal```

Run `setup.py` python file. It will install all the dependencies for the project in a virtual environment by the name `py-env` and also install the postgresql database.
```python setup.py```

##### Set up the database
After cloning the project and installing all the dependencies, open a new terminal window and log into postgresql server
```sudo -i -u postgres```

Go into the postgresql shell by typing
```psql```

Now create a database by the name `attendance_portal`
```createdb attendance_portal;```

You can check that you database has been created by typing `\l`.
The database `attendance_portal` will be in the list of local databases.

You can follow this link if you want to create a new user for this project to log into the postgresql server - [Install and use postgresql - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04#installation)

After setting up the database, you would need to put your password for the postgresql server which you put in during installation of postgresql in a bash file. Open a new terminal window and type
```vim .my_profile```
and then write
```export postgres_password="Insert your postgres password here"```
and execute this file with
```source .my_profile```

>You would need to run the above command every time you restart your system to access the database


After doing all the abovementioned tiresome things, there is just one more thing to do. Migrate the database schema and create all the tables. For that, go into your project directory with virtaulenv enabled and type
```python manage.py makemigrations```
```python manage.py migrate```

## Start the server
You can start the server by writing the command
```python manage.py runserver```