# Hearts

## First time project setup

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

### Getting new changes

To get new changes to the repository (usually you do this every time you start
working) run

```
git pull
```

If your git starts outputting strange messages and you want to reset it (at the
cost of losing any local changes) run

```
git reset --hard origin/master
```

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

## Testing

Use `py.test` to run the test suite. This will find all files starting with
`test` in the repository and run them. All functions in these files starting
with `test_` will be run as tests, and failing tests will produce a stack
trace.

## Running a local server

Test to see if the server is working by running

```
python app.py
```

and browse to `http://127.0.0.1:5000/`.
