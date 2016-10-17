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
