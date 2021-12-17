# Entertainment Recommendation Website
Once upon a time, We'll work under the "store" directory


in elkhan/settings.py:

change your correct USER/PASSWORD/HOST/PORT.
The default one follows exactly what Assignment 2 does.
```json
{
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "xe",
        "USER": "unist",
        "PASSWORD": "unist",
        "HOST": "127.0.0.1", 
        "PORT": "1521"
    }
}
```
### Install dependencies
```bash
    pip install -r requirements.txt
```
### How to Run
Run the server and go to http://localhost:8000/store/
```bash
    python manage.py runserver
```
