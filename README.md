# Hearts

## First time project setup

Run the following from the command line

```
git clone git@github.com:j2kun/lonely-hearts.git
cd lonely-hearts
virtualenv -p python3 venv  

# on Mac/Linux
source venv/bin/activate

# on Windows
. venv/Scripts/activate

pip install -r requirements.txt
```

Test to see if the server is working by running

```
python app.py
```

and browse to `http://127.0.0.1:5000/`.
