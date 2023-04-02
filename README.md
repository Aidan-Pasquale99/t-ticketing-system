<!-- TODO: (nice to do) clean up unused imports -->
<!-- TODO: Due date should not be able to be prior to current date -->
# Temenos Ticketing System

## Overview

This Temenos Ticketing System is a Flask-based web application which utilises the SQLAlchemy, Flask Login and Flask WTForms libraries to provide a simple ticket management system for tracking work items. It has functionality to register new non-admin users. By default, there is a standard user and administrator user. Standard users can create and update tickets, and admin users can create, update and additionally delete tickets.

## Running

### Prerequisites

The following need to be installed in your shell before the application can be run:

- python3
- pip

Once the above are installed, execute the following command to install all required libraries (it is required to run this within the `temenos-ticketing-system` directory, or alternatively provide the absolute path to the `requirements.txt` file):
```
pip -r requirements.txt
```

### Starting the application

Set the following variables in your terminal substituting the $PLACEHOLDER value with a value of your choosing:
```
export SECRET_KEY=$PLACEHOLDER
export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL=sqlite:///db.sqlite
export FLASK_APP=src
```

### Accessing the Application

Run the following command in the `temenos-ticketing-system` directory:
```
python3 manage.py run
```

Then go to `http://127.0.0.1:5000` in a web browser.

From here, you can register a new user by clicking `Register now`