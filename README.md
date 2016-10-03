# Hearts

## First time project setup

Run the following from the command line

```
git clone git@github.com:j2kun/lonely-hearts.git
cd lonely-hearts
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Test to see if the server is working by running

```
python manage.py migrate
python manage.py runserver
```

and browse to `http://127.0.0.1:8000/`.
