# Hearts 
[![travis-badge](https://travis-ci.org/j2kun/lonely-hearts.svg?branch=master)](https://travis-ci.org/j2kun/lonely-hearts) [![Coverage Status](https://coveralls.io/repos/github/j2kun/lonely-hearts/badge.svg)](https://coveralls.io/github/j2kun/lonely-hearts)

## First time project setup

### Set up python requirements

Run the following from the command line

```
git clone git@github.com:j2kun/lonely-hearts.git
cd lonely-hearts
virtualenv -p python3.5 venv  

# on Mac/Linux
source venv/bin/activate

# on Windows
. venv/Scripts/activate

pip install -r requirements.txt
```

### Set up database

First install the mongo database and `mongod` (daemon that runs the database)
from the [mongodb website](https://www.mongodb.com/). For OS X, you can run

```
brew install mongodb
```

Then create the local data directory for the database.

```
mkdir -p data/db
```

### Setting up .env

Configuration variables are read from a file called `.env` in the base
directory of the project. This repository includes a `env.template` file to
serve as a guide. **Do not** check in your `.env` to the repository (make sure
it is in the `.gitignore` file), since in general it contains secret keys that
are not public.

```
cp env.template .env
vim .env  # edit to set configuration variables for your environment
```

For example, if you're developing on Cloud9, you'd need to set

```
HOST=0.0.0.0
PORT=8080
```

These configuration variable are loaded into the environment using the `dotenv`
package in `settings.py`.


## Testing

Use `py.test` to run the test suite. This will find all files starting with
`test` in the repository and run them. All functions in these files starting
with `test_` will be run as tests, and failing tests will produce a stack
trace.

## Running a local server

Start the database

```
mongod --dbpath data/db
```

In a separate terminal window, run the web app

```
python app.py
```

and browse to `http://127.0.0.1:5000/`.

### Fixing problems

To delete and recreate your virtual envrionment, run the following
from the base directory of the project.

```
deactivate
rm -rf venv
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
```
